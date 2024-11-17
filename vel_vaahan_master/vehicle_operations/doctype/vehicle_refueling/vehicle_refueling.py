# Copyright (c) 2024, SMTW and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class VehicleRefueling(Document):

	def sanitize_inputs(self):
		if not self.adjustment_amount:
			self.adjustment_amount = 0

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

	def check_duplicate_vaahan(self):
		v_list = [v.vaahan for v in self.vehicle_details]
		if len(set(v_list)) != len(v_list):
			frappe.throw("Duplicated Vaahan in Vehicle Details.")

	def validate(self):
		self.validate_fuel_type()
		self.validate_fuel_rate()
		self.check_duplicate_vaahan()

	def update_calculated_fields(self):
		self.total_qty = sum([v.fuel_qty for v in self.vehicle_details])
		self.invoice_amount = round(self.total_qty * self.fuel_rate + self.adjustment_amount, 2)

	def before_save(self):
		self.sanitize_inputs()
		self.update_calculated_fields()
