# Copyright (c) 2024, SMTW and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class VehicleRefueling(Document):
	def validate_fuel_type(self):
		fuel_error = []
		for detail in self.vehicle_details:
			v = frappe.get_doc("Vaahan", detail.vaahan)
			vm = frappe.get_doc("Vehicle Model", v.model)
			if self.fuel != vm.fuel:
				fuel_error.append(detail.idx)
		frappe.throw("Fuel type of document is {}, but vehicle(s) in No. {} is/are of different fuel.".format(
					self.fuel, fuel_error))

	def validate_fuel_rate(self):
		if self.fuel_rate <= 0:
			frappe.throw("Fuel Rate must be greater than 0.")

	def validate(self):
		self.validate_fuel_type()
		self.validate_fuel_rate()

	def update_calculated_fields(self):
		self.total_qty = sum([v.fuel_qty for v in self.vehicle_details])
		self.invoice_amount = round(self.total_qty * self.fuel_rate + self.adjustment_amount, 2)

	def before_save(self):
		self.update_calculated_fields()
