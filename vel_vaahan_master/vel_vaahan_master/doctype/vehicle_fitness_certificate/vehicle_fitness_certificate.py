# Copyright (c) 2024, SMTW and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
import frappe


class VehicleFitnessCertificate(Document):


	def validate_dates(self):
		if self.inspected_on >= self.next_inspection:
			frappe.throw('Inspection date should be before next inspection date.')
		if self.next_inspection >= self.valid_till:
			frappe.throw('Next Inspection date should be before Valid Till date.')

	def validate(self):
		self.validate_dates()

	def on_update(self):
		def update_vehicle_details(veh):
			v = frappe.get_doc("Vaahan", veh)
			v.update_fc_details()

		update_vehicle_details(self.vaahan)
		old_doc = self.get_doc_before_save()
		if old_doc and old_doc.vaahan != self.vaahan:
				update_vehicle_details(old_doc.vaahan)
