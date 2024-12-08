# Copyright (c) 2024, SMTW and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import date_diff, time_diff


class PassengerVehicleTrip(Document):

	def sanitize_fields(self):
		if self.on_fixed_route:
			self.trip_segments = []
		else:
			self.route = self.end_km = self.end_datetime = None

	def get_fixed_route_start(self):
		if not self.on_fixed_route:
			return
		r = frappe.get_doc('Vehicle Route', self.route)
		self.start_from = r.route_stops[0].stop_name if not self.reverse_dir \
														else r.route_stops[-1].stop_name

	def validate_route(self):
		if not self.on_fixed_route:
			return
		if self.end_km <= self.start_km:
			frappe.throw("End KM must be greater than start KM.")
		if self.end_datetime <= self.start_datetime:
			frappe.throw("End datetime must be greater than start datetime.")

	def get_route_km(self):
		km = frappe.db.get_value("Vehicle Route", self.route, 'total_km')
		return km

	def calculate_trip_details(self):
		if not self.on_fixed_route:
			self.route_km = self.route_difference = 0
			if self.trip_segments:
				self.total_km = self.trip_segments[-1].end_km - self.start_km
				self.total_time = time_diff(self.trip_segments[-1].end_datetime, self.start_datetime).total_seconds() / 3600
		else:
			self.total_km = self.end_km - self.start_km
			self.total_time = time_diff(self.end_datetime, self.start_datetime).total_seconds() / 3600
			route_km = self.get_route_km()
			self.route_km = route_km
			self.route_difference = self.total_km - route_km


	def validate_start_odometer(self):
		if self.start_km < 0:
			frappe.throw("Start Km must be greater than 0.")

	def validate_trip_segments(self):
		if self.on_fixed_route:
			return

		if not self.trip_segments:
			frappe.throw("No trip segments have been created.")
		last_seg = self.trip_segments[-1]

		if not last_seg or not last_seg.end_km or not last_seg.end_datetime:
			frappe.throw('Last segment must contain End KM, End Datetime.')

		prev_km = self.start_km
		for seg in self.trip_segments:
			if seg.end_km and prev_km and prev_km > seg.end_km:
				frappe.throw(f'End KM must be greater than Start / previous End KM: No. {seg.idx}')
			prev_km = seg.end_km

		if self.total_km <= 0:
			frappe.throw('Total KM must be greater than 0.')

	def update_vaahan_odo(self):
		max_odo = self.trip_segments[-1].end_km if not self.on_fixed_route else self.end_km
		v = frappe.get_doc("Vaahan", self.vaahan)
		v.update_odometer(max_odo)

	def before_save(self):
		self.sanitize_fields()
		self.get_fixed_route_start()
		self.calculate_trip_details()
		pass

	def validate(self):
		self.validate_route()
		self.validate_start_odometer()

	def before_submit(self):
		self.validate_trip_segments()

	def on_submit(self):
		self.update_vaahan_odo()

	def on_cancel(self):
		v = frappe.get_doc("Vaahan", self.vaahan)
		v.update_odometer(-1)
