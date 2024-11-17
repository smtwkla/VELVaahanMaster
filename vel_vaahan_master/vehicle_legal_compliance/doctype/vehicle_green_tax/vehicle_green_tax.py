# Copyright (c) 2024, SMTW and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class VehicleGreenTax(Document):
	def validate_dates(self):
		if self.from_date >= self.till_date:
			frappe.throw('Till date should be after From date.')

	def validate_vehicle_requires_green_tax(self):
		veh = frappe.get_doc("Vaahan", self.vaahan)
		if not veh.green_tax_applicable:
			frappe.throw(f'Vaahan {veh} does not require permit.')

	def validate(self):
		self.validate_dates()
		self.validate_vehicle_requires_green_tax()

	def on_update(self):
		def update_vehicle_details(veh):
			v = frappe.get_doc("Vaahan", veh)
			v.update_green_tax_details()

		update_vehicle_details(self.vaahan)
		old_doc = self.get_doc_before_save()
		if old_doc and old_doc.vaahan != self.vaahan:
			update_vehicle_details(old_doc.vaahan)

