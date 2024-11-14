# Copyright (c) 2024, SMTW and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class VehicleTyre(Document):
	def validate(self):
		if self.purchase_price < 0:
			frappe.throw("Purchase Price must be greater than 0.")
