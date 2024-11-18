# Copyright (c) 2024, SMTW and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
from frappe.model.naming import getseries


class VehicleDriver(Document):
	def autoname(self):
		prefix = 'V-DRV-'
		sl = getseries(prefix,4)
		self.name = f'{prefix}{sl}'
		self.gen_title = f'{self.driver_name} {self.name}'
