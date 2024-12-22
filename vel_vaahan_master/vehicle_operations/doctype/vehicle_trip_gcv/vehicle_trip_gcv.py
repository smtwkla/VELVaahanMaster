# Copyright (c) 2024, SMTW and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import date_diff, time_diff
from datetime import datetime, timedelta

class VehicleTripGCV(Document):

	def sanitize_trip_details(self):
		for seg in self.trip_segments:
			if seg.seg_type != 'Travel To':
				seg.end_km = None
				seg.travel_to = None
			else:
				seg.load_weight = None

	def validate_vehicle_type(self):
		v = frappe.get_doc("Vaahan", self.vaahan)
		vm = frappe.get_doc("Vehicle Model", v.model)
		if not vm.is_gv:
			frappe.throw("Vehicle Model {} is not Goods Vehicle".format(v.model))

	def validate_odometer(self):
		if self.start_km < 0:
			frappe.throw("Start Km must be greater than 0.")

		for seg in self.trip_segments:
			if seg.seg_type == 'Travel To':
				if seg.end_km <= self.start_km:
					frappe.throw("End Km of Trip Segment No. {} must be greater than start Km".format(
									seg.idx))
		def check_overlap(km, km2=None):
			"""Returns conflicting trip if exists, else None."""
			if not km2:
				boundary_condition = f"AND start_km < {km} AND (vtg.start_km + vtg.total_km) > {km}"
			else:
				boundary_condition = f"AND start_km > {km} AND (vtg.start_km + vtg.total_km) < {km2}"

			csql = f"""
			SELECT vtg.name
	            FROM `tabVehicle Trip GCV` vtg
	            WHERE vtg.vaahan ='{self.vaahan}'
	            {boundary_condition}
	            AND vtg.docstatus = 1;
			"""
			res = frappe.db.sql(csql)
			if res:
				return res[0][0]

		if conflicting_trip:=check_overlap(self.start_km):
			frappe.throw(
				f"Trip start Km {self.start_km} is within the range of completed trip {conflicting_trip}.")

		try:
			end_km = max([x.end_km for x in self.trip_segments if x.seg_type == 'Travel To'])
			if conflicting_trip:=check_overlap(end_km):
				frappe.throw(
					f"Trip end Km {end_km} is within the range of completed trip {conflicting_trip}.")
			if conflicting_trip:=check_overlap(self.start_km, end_km):
				frappe.throw(
					f"Trip odometer range is conflicts with the range of completed trip {conflicting_trip}.")
		except ValueError:
			pass



	def validate_trip_details_for_submit(self):
		if not [s.idx for s in self.trip_segments if s.seg_type == 'Travel To']:
			frappe.throw("There must be at least one Travel To segment.")

	def validate_trip_details(self):

		f_errors = [s.idx for s in self.trip_segments if (s.seg_type != 'Unloading' and s.freight_collected)]
		if f_errors:
			frappe.throw(f'Freight collected must be entered in Unloading segments only: {f_errors}')

		f_errors = [s.idx for s in self.trip_segments if
		            (s.seg_type == 'Travel To' and not s.travel_to)]
		if f_errors:
			frappe.throw(f'Travel To segments must contain location: {f_errors}')

		f_errors = [s.idx for s in self.trip_segments if
		            (s.seg_type in ['Loading', 'Unloading'] and not s.load_weight)]
		if f_errors:
			frappe.throw(f'Segments for Loading and Unloading must have Load Weight: {f_errors}')

		def str_to_dt(s):
			if not s:
				frappe.throw("Please enter End time in all segments.")
			return datetime.strptime(s, "%Y-%m-%d %H:%M:%S")

		prev_time = str_to_dt(self.start_datetime)
		prev_km = self.start_km
		for seg in self.trip_segments:
			seg_time = str_to_dt(seg.end_datetime)
			if prev_time >= seg_time:
				frappe.throw(f'End Time must be greater than Start / previous End Time: No. {seg.idx}')
			if prev_km and seg.end_km and prev_km >= seg.end_km:
				frappe.throw(f'End KM must be greater than Start / previous End KM: No. {seg.idx}')
			prev_time = seg_time
			prev_km = seg.end_km

	def calculate_trip_details(self):
		if not self.trip_segments:
			return
		total_amt = 0
		prev_km = self.start_km
		prev_dt = self.start_datetime
		travel_time = loading_time = unloading_time = waiting_time = timedelta(seconds=0)
		last_km = None

		for seg in self.trip_segments:

			if seg.freight_collected:
				total_amt += seg.freight_collected

			if seg.seg_type == 'Travel To':
				last_km = seg.end_km
				travel_time = travel_time + time_diff(seg.end_datetime, prev_dt)
				prev_km = seg.end_km
			elif seg.seg_type == 'Loading':
				loading_time = loading_time + time_diff(seg.end_datetime, prev_dt)

			elif seg.seg_type == 'Unloading':
				unloading_time = unloading_time + time_diff(seg.end_datetime, prev_dt)

			elif seg.seg_type == 'Waiting':
				waiting_time = waiting_time + time_diff(seg.end_datetime, prev_dt)

			prev_dt = seg.end_datetime

		self.total_km = (last_km - self.start_km) if last_km else None
		self.total_freight = total_amt
		self.travel_time = travel_time.total_seconds() / 3600
		self.loading_time = loading_time.total_seconds() / 3600
		self.unloading_time = unloading_time.total_seconds() / 3600
		self.waiting_time = waiting_time.total_seconds() / 3600

	def validate(self):
		self.validate_odometer()
		self.validate_trip_details()
		self.validate_vehicle_type()

	def before_save(self):
		self.sanitize_trip_details()
		self.calculate_trip_details()

	def before_submit(self):
		self.validate_trip_details_for_submit()

	def on_submit(self):
		max_odo = max([s.end_km for s in self.trip_segments if s.seg_type == 'Travel To'])
		v = frappe.get_doc("Vaahan", self.vaahan)
		v.update_odometer(max_odo)

	def on_cancel(self):
		v = frappe.get_doc("Vaahan", self.vaahan)
		v.update_odometer(-1)
