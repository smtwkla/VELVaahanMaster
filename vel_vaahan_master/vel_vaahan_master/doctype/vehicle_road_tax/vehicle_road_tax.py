# Copyright (c) 2024, SMTW and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class VehicleRoadTax(Document):
	def validate_dates(self):
		if self.from_date >= self.till_date:
			frappe.throw('Road Tax Till date should be after From date.')

	def validate_vehicle_requires_road_tax(self):
		veh = frappe.get_doc("Vaahan", self.vaahan)
		if not veh.requires_road_tax():
			frappe.throw(f'Vehicle model {veh.model} does not require road tax.')

	def validate(self):
		self.validate_dates()
		self.validate_vehicle_requires_road_tax()

	def on_update(self):
		def update_vehicle_details(veh):
			v = frappe.get_doc("Vaahan", veh)
			v.update_road_tax_details()

		update_vehicle_details(self.vaahan)
		old_vaahan = self.get_doc_before_save().vaahan
		if old_vaahan != self.vaahan:
			update_vehicle_details(old_vaahan)
