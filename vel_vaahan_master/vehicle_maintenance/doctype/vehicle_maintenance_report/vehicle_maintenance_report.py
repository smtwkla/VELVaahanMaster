# Copyright (c) 2024, SMTW and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, date_diff, get_datetime


class VehicleMaintenanceReport(Document):
	def check_duplicate_invoices(self):
		inv = [(i.vendor, i.invoice_number, i.invoice_date) for i in self.invoices ]
		if len(inv) != len(set(inv)):
			frappe.throw("Duplicate Invoice entries found")

		inv = [(i.vendor, i.invoice_number) for i in self.invoices ]
		if len(inv) != len(set(inv)):
			frappe.throw("Same Invoice(s) entered with different Invoice Date found")

	def check_maintenance_activities_dates(self):
		if not self.end_datetime:
			frappe.throw("End Datetime not entered")

		doc_end_datetime = get_datetime(self.end_datetime)
		doc_start_datetime = get_datetime(self.start_datetime)

		if doc_end_datetime < doc_start_datetime:
			frappe.throw("Maintenance Start Datetime must be before End Datetime")

		for a in self.activities:
			if not a.end_datetime or not a.start_datetime:
				frappe.throw("Maintenance Activity Start/End Datetime missing: {}".format(a.idx))
			if doc_start_datetime > get_datetime(a.start_datetime):
				frappe.throw("Activity {} starts before Start datetime".format(a.idx))
			if doc_end_datetime < get_datetime(a.end_datetime):
				frappe.throw("Activity {} ends after End datetime".format(a.idx))

	def calculate_duration(self):
		if self.end_datetime:
			self.total_days = round((get_datetime(self.end_datetime) - get_datetime(self.start_datetime)).total_seconds() / 86400 ,1)
		else:
			self.total_days = None

	def calculate_invoice_details(self):
		total = 0
		for i in self.invoices:
			i.invoice_amt = i.invoice_gross_amt + i.gst_amt
			total += i.invoice_amt
		self.total_amt = total

	def before_save(self):
		self.calculate_invoice_details()
		self.calculate_duration()

	def before_submit(self):
		self.check_maintenance_activities_dates()
		if len(self.activities) == 0:
			frappe.throw("No Maintenance Activities entered")

	def validate(self):
		self.check_duplicate_invoices()

