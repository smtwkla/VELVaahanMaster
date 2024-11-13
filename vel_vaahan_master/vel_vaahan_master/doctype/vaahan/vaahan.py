# Copyright (c) 2024, SMTW and contributors
# For license information, please see license.txt

import re
from datetime import datetime

import frappe
from frappe.model.document import Document
from frappe.utils import (getdate, add_months, today)


class Vaahan(Document):

	def requires_permit(self):
		return frappe.get_doc("Vehicle Model", self.model).permit_required


	def requires_road_tax(self):
		return frappe.get_doc("Vehicle Model", self.model).road_tax_required


	def update_green_tax_applicability(self):
		if not self.green_tax_applicable:
			if self.manufacture_mon_yr:
				mon = int(self.manufacture_mon_yr[0:2])
				year = int(self.manufacture_mon_yr[3:])
				age = (datetime.now() - datetime(year, mon, 1)).days / 365
				if (self.registration_type == 'Commercial' and age > 8) or \
						(self.registration_type == 'Personal' and age > 15) :
					self.green_tax_applicable = True


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
			if (not self.road_tax_valid_till) or getdate(self.road_tax_valid_till) <= getdate(today()):
				road_tax_status = "Urgent"
				status_txt += "Road Tax validity expired / not available. "
			elif getdate(self.road_tax_valid_till) <= getdate(add_months(today(), 1)):
				road_tax_status = "Pending"
				status_txt += "Road Tax validity expiring soon. "
			else:
				road_tax_status = "OK"
		else:
			road_tax_status = None

		if self.green_tax_applicable:
			if (not self.green_tax_valid_till) or getdate(self.green_tax_valid_till) <= getdate(today()):
				green_tax_status = "Urgent"
				status_txt += "Green Tax validity expired / not available. "
			elif getdate(self.green_tax_valid_till) <= getdate(add_months(today(), 1)):
				green_tax_status = "Pending"
				status_txt += "Green Tax validity expiring soon. "
			else:
				green_tax_status = "OK"

		else:
			green_tax_status = None

		if getdate(self.puc_valid_till) <= getdate(today()):
			puc_status = "Urgent"
			status_txt += "PUC Expired. "
		elif getdate(self.puc_valid_till) <= getdate(add_months(today(), 1)):
			puc_status = "Pending"
			status_txt += "PUC expiring soon. "
		else:
			puc_status = "OK"

		if fc_status == "Urgent" or insurance_status == "Urgent" or permit_status == "Urgent" or \
				road_tax_status == "Urgent" or green_tax_status == "Urgent" or puc_status == "Urgent":
			self.status = "Urgent"
		elif fc_status == "Pending" or insurance_status == "Pending" or permit_status == "Pending" \
				or road_tax_status == "Pending" or green_tax_status == "Pending" or puc_status == "Pending":
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


	def update_green_tax_details(self):
		if self.green_tax_applicable:
			gt = frappe.db.get_list(
								'Vehicle Green Tax',
			                    filters={'vaahan':self.name},
								fields=['name','till_date'],
			                    order_by='till_date desc',
			                    limit=1
			                   )
			self.green_tax_valid_till = gt[0].till_date if gt else None
		else:
			self.green_tax_valid_till = None
		self.save()


	def update_puc_details(self):
		puc = frappe.db.get_list(
							'Vehicle Pollution Under Control Certificate',
		                    filters={'vaahan':self.name},
							fields=['name','till_date'],
		                    order_by='till_date desc',
		                    limit=1
		                   )
		self.puc_valid_till = puc[0].till_date if puc else None
		self.save()


	def before_save(self):
		self.update_green_tax_applicability()
		self.update_status()


	def validate_mfr_date(self):
		pattern = r"^(0[1-9]|1[0-2])-\d{4}$"

		if not re.match(pattern, self.manufacture_mon_yr):
			frappe.throw(f'Month-Year of Manufacture must be in mm-yyyy format.')


	def validate(self):
		self.validate_mfr_date()


	def run_daily_scheduled_tasks(self):
		self.update_green_tax_applicability()
		self.update_status()
		self.save()
