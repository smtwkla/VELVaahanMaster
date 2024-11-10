# Copyright (c) 2024, SMTW and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Vaahan(Document):

	def update_fc_details(self):
		fc = frappe.db.get_list(
							'Vehicle Fitness Certificate',
		                    filters={'vaahan':self.name},
							fields=['name','valid_till','next_inspection'],
		                    order_by='valid_till desc',
		                    limit=1
		                   )
		self.fc_valid_till = fc[0].valid_till
		self.fc_insp_due = fc[0].next_inspection
		self.save()
