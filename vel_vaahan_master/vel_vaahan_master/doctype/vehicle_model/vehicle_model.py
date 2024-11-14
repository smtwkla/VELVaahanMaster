# Copyright (c) 2024, SMTW and contributors
# For license information, please see license.txt
from tabnanny import check

import frappe
from frappe.model.document import Document


class VehicleModel(Document):
	def before_save(self):
		self.payload = self.gvw - self.uvw

	def check_weights(self):
		if self.gvw < self.uvw:
			frappe.throw("Vehicle gross weight cannot be lesser than unladen weight.")

	def validate(self):
		self.check_weights()
