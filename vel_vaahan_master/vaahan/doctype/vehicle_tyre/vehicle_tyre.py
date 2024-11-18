# Copyright (c) 2024, SMTW and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class VehicleTyre(Document):
	def validate(self):
		if not self.purchase_price:
			frappe.throw("Purchase Price must be greater than 0.")

	def set_title(self):
		tyre_model = frappe.db.get_value('Tyre Model', self.tyre_model, 'tyre_model')
		self.title = f'{self.serial}-{tyre_model}'

	def before_save(self):
		self.set_title()

