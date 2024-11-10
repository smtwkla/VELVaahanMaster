# Copyright (c) 2024, SMTW and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
import frappe


class VehicleInsurancePolicy(Document):
	def validate(self):
		if self.from_date >= self.till_date:
			frappe.throw('From date should be before Till date.')
