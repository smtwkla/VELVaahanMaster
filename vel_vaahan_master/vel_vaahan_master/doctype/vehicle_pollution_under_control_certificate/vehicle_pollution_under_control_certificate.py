# Copyright (c) 2024, SMTW and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class VehiclePollutionUnderControlCertificate(Document):
	def on_update(self):
		def update_vehicle_details(veh):
			v = frappe.get_doc("Vaahan", veh)
			v.update_puc_details()

		update_vehicle_details(self.vaahan)
		old_doc = self.get_doc_before_save()
		if old_doc and old_doc.vaahan != self.vaahan:
			update_vehicle_details(old_doc.vaahan)

