# Copyright (c) 2024, SMTW and contributors
# For license information, please see license.txt


from datetime import datetime

import frappe
from frappe.model.document import Document
from frappe.utils import time_diff

class EquipmentUsageRecord(Document):
	def sanitize_trip_details(self):
		pass

	def validate_vehicle_type(self):
		v = frappe.get_doc("Vaahan", self.vaahan)
		vm = frappe.get_doc("Vehicle Model", v.model)
		if vm.odometer_type != "Hour Meter":
			frappe.throw("Vehicle Model {} is not Vehicle with Hour Meter".format(v.model))

	def validate_odometer(self):
		if self.start_hourmeter < 0:
			frappe.throw("Start Hour Meter must be greater than 0.")

		for seg in self.usage_details:
			if seg.end_hourmeter and seg.end_hourmeter <= self.start_hourmeter:
				frappe.throw(
					"End Hour Meter of Usage Details No. {} must be greater than Start Hour Meter".format(
						seg.idx))
			if seg.end_datetime and seg.end_datetime <= self.start_datetime:
				frappe.throw(
					"End Datetime of Usage Details No. {} must be greater than Start Datetime".format(
						seg.idx))

	def validate_trip_details_for_submit(self):
		if not len(self.usage_details):
			frappe.throw("There must be at least one Usage Details line.")

		if not self.usage_details[-1].end_hourmeter or not self.usage_details[-1].end_datetime:
			frappe.throw(
				"The last line of Usage Details must contain End Hour Meter and End Datetime.")

	def validate_trip_details(self):

		prev_time = datetime.strptime(self.start_datetime, "%Y-%m-%d %H:%M:%S")
		prev_hm = self.start_hourmeter
		for seg in self.usage_details:
			if seg.end_datetime:
				seg_time = datetime.strptime(seg.end_datetime, "%Y-%m-%d %H:%M:%S")
				if seg_time and prev_time >= seg_time:
					frappe.throw(
						f'End Time must be greater than Start / previous End Time: No. {seg.idx}')
			if seg.end_hourmeter and prev_hm >= seg.end_hourmeter:
				frappe.throw(
					f'End Hour Meter must be greater than Start / previous End Hour Meter: No. {seg.idx}')
			prev_time = seg_time if seg_time else prev_time
			prev_hm = seg.end_hourmeter if seg.end_hourmeter else prev_hm

	def calculate_trip_details(self):
		if (not self.usage_details or not self.usage_details[-1].end_hourmeter
				or not self.usage_details[-1].end_datetime):
			self.usage_duration = self.total_run_hrs = 0
			return

		usage_duration = time_diff(self.usage_details[-1].end_datetime, self.start_datetime)
		self.usage_duration = usage_duration.total_seconds() / 3600
		self.total_run_hours = self.usage_details[-1].end_hourmeter - self.start_hourmeter

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
		v = frappe.get_doc("Vaahan", self.vaahan)
		v.update_odometer(self.usage_details[-1].end_hourmeter)

	def on_cancel(self):
		v = frappe.get_doc("Vaahan", self.vaahan)
		v.update_odometer(-1)
