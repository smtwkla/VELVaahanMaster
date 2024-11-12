# Copyright (c) 2024, SMTW and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import (getdate, add_months, today)


class Vaahan(Document):

	def requires_permit(self):
		return frappe.get_doc("Vehicle Model", self.model).permit_required

	def requires_road_tax(self):
		return frappe.get_doc("Vehicle Model", self.model).road_tax_required

	def update_status(self):
		status_txt = ""
		if getdate(self.fc_valid_till) <= getdate(today()):
			fc_status = "Urgent"
			status_txt += "FC not valid. "
		elif (getdate(self.fc_valid_till) <= getdate(add_months(today(), 1)) or
		      getdate(self.fc_insp_due) <= getdate(today())):
			fc_status = "Pending"
			status_txt += "FC Inspection due / validity expiring soon. "
		else:
			fc_status = "OK"

		if getdate(self.insurance_valid_till) <= getdate(today()):
			insurance_status = "Urgent"
			status_txt += "Insurance Expired. "
		elif getdate(self.insurance_valid_till) <= getdate(add_months(today(), 1)):
			insurance_status = "Pending"
			status_txt += "Insurance expiring soon. "
		else:
			insurance_status = "OK"

		if self.requires_permit():
			if getdate(self.permit_valid_till) <= getdate(today()):
				permit_status = "Urgent"
				status_txt += "Permit Expired. "
			elif getdate(self.permit_valid_till) <= getdate(add_months(today(), 1)):
				permit_status = "Pending"
				status_txt += "Permit expiring soon. "
			else:
				permit_status = "OK"
		else:
			permit_status = None

		if self.requires_road_tax():
			if getdate(self.road_tax_valid_till) <= getdate(today()):
				road_tax_status = "Urgent"
				status_txt += "Road Tax validity expired. "
			elif getdate(self.road_tax_valid_till) <= getdate(add_months(today(), 1)):
				road_tax_status = "Pending"
				status_txt += "Road Tax validity expiring soon. "
			else:
				road_tax_status = "OK"
		else:
			road_tax_status = None

		if fc_status == "Urgent" or insurance_status == "Urgent" or permit_status == "Urgent" or road_tax_status == "Urgent":
			self.status = "Urgent"
		elif fc_status == "Pending" or insurance_status == "Pending" or permit_status == "Pending" or road_tax_status == "Pending":
			self.status = "Pending"
		else:
			self.status = "OK"

		self.status_txt = status_txt


	def update_fc_details(self):
		fc = frappe.db.get_list(
							'Vehicle Fitness Certificate',
		                    filters={'vaahan':self.name},
							fields=['name','valid_till','next_inspection'],
		                    order_by='valid_till desc',
		                    limit=1
		                   )
		self.fc_valid_till = fc[0].valid_till if fc else None
		self.fc_insp_due = fc[0].next_inspection if fc else None
		self.save()


	def update_insurance_details(self):
		insurance = frappe.db.get_list(
							'Vehicle Insurance Policy',
		                    filters={'vaahan':self.name},
							fields=['name','till_date'],
		                    order_by='till_date desc',
		                    limit=1
		                   )
		self.insurance_valid_till = insurance[0].till_date if insurance else None
		self.save()


	def update_permit_details(self):
		permit = frappe.db.get_list(
							'Vehicle Permit',
		                    filters={'vaahan':self.name},
							fields=['name','till_date'],
		                    order_by='till_date desc',
		                    limit=1
		                   )
		self.permit_valid_till = permit[0].till_date if permit else None
		self.save()


	def update_road_tax_details(self):
		rt = frappe.db.get_list(
							'Vehicle Road Tax',
		                    filters={'vaahan':self.name},
							fields=['name','till_date'],
		                    order_by='till_date desc',
		                    limit=1
		                   )
		self.road_tax_valid_till = rt[0].till_date if rt else None
		self.save()

	def before_save(self):
		self.update_status()
