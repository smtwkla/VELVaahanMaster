# Copyright (c) 2024, SMTW and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class VehicleRoute(Document):
	def set_title(self):
		self.title = f'{self.route_code}-{self.route_name}'

	def update_calculated_fields(self):
		self.stop_count = len(self.route_stops)
		if self.route_stops:
			self.total_km = self.route_stops[-1].km

	def before_save(self):
		self.set_title()
		self.update_calculated_fields()

	def validate_segments(self):
		if not self.route_stops:
			frappe.throw("Please enter route stops.")

		last_km = None
		for s in self.route_stops:
			if last_km is None:
				if s.km != 0:
					frappe.throw("First stop is starting point and must have 0 km.")
			else:
				if s.km < last_km:
					frappe.throw("KM must be increasing: No.{}".format(s.idx))
			last_km = s.km

	def validate(self):
		self.validate_segments()
