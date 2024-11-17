# Copyright (c) 2024, SMTW and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import date_diff, time_diff


class PassengerVehicleTrip(Document):

	def calculate_trip_details(self):
		if self.trip_segments:
			self.total_km = self.trip_segments[-1].end_km - self.start_km
			self.total_time = time_diff(self.trip_segments[-1].end_datetime, self.start_datetime).total_seconds() / 3600

			print(self.trip_segments[-1].end_datetime, self.start_datetime)

	def validate_odometer(self):
		if self.start_km < 0:
			frappe.throw("Start Km must be greater than 0.")
		prev_km = self.start_km
		for seg in self.trip_segments:
			if seg.end_km and prev_km and prev_km >= seg.end_km:
				frappe.throw(f'End KM must be greater than Start / previous End KM: No. {seg.idx}')
			prev_km = seg.end_km

	def validate_last_segment(self):
		if not self.trip_segments:
			return
		last_seg = self.trip_segments[-1]
		if not last_seg or not last_seg.end_km or not last_seg.end_datetime:
			frappe.throw('Last segment must contain End KM, End Datetime.')

	def before_save(self):
		self.calculate_trip_details()

	def validate(self):
		self.validate_odometer()
		self.validate_last_segment()
