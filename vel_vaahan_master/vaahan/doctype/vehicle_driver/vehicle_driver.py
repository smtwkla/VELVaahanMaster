# Copyright (c) 2024, SMTW and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.naming import getseries
from frappe.utils.file_manager import get_file_name

class VehicleDriver(Document):
	def autoname(self):
		prefix = 'V-DRV-'
		sl = getseries(prefix,4)
		self.name = f'{prefix}{sl}'
		self.title = f'{self.driver_name} [{self.name}]'

	def before_save(self):
		if self.attach_driver_image:
			fn = get_file_name(self.attach_driver_image,"-s-")
			print(fn, self.attach_driver_image)
		self.title = f'{self.driver_name} [{self.name}]'
