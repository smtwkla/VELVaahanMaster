# Copyright (c) 2024, SMTW and contributors
# For license information, please see license.txt

from _datetime import datetime, timedelta
from turtledemo.penrose import start

import frappe
from frappe.model.document import Document
from frappe.utils import date_diff, time_diff


class GoodsVehicleTrip(Document):
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

		start_time = str_to_dt(self.start_datetime)
		for seg in self.trip_segments:
			seg_time = str_to_dt(seg.end_datetime)
			if start_time >= seg_time:
				frappe.throw(f'End Time must be greater than Start Datetime: {seg.idx}')
			start_time = seg_time

	def calculate_trip_details(self):
		if not self.trip_segments:
			return
		total_amt = 0
		prev_km = self.start_km
		prev_dt = self.start_datetime
		travel_time = loading_time = unloading_time = waiting_time = timedelta(seconds=0)

		for seg in self.trip_segments:
			last_km = None
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

	def on_submit(self):
		max_odo = max([s.end_km for s in self.trip_segments if s.seg_type == 'Travel To'])
		v = frappe.get_doc("Vaahan", self.vaahan)
		v.update_odometer(max_odo)

	def on_cancel(self):
		v = frappe.get_doc("Vaahan", self.vaahan)
		v.update_odometer(-1)
