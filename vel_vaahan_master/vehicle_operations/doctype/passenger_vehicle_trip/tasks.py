import frappe
from frappe.model.docstatus import DocStatus
from frappe.utils.background_jobs import enqueue
from frappe.utils import add_to_date, date_diff

from pprint import pprint
from datetime import date, timedelta


class PVTConditionEmail:
	PV_TRIP_CONDITION_TEMPLATE = "Passenger Vehicle Condition Feedback Report"
	MAX_REPORT_RUNS_PER_DAY = 100

	def __init__(self, date_of_report):
		self.email_to = None
		self.subject = None
		self.remarks = []
		self.date_of_report = date_of_report
		self.email_template = frappe.get_doc("Email Template", self.PV_TRIP_CONDITION_TEMPLATE)

	def load_trips(self):
		dt_start = self.date_of_report + ' 00:00:00'
		dt_end = self.date_of_report + ' 23:59:59.999999'
		trips = frappe.db.get_list(
			"Passenger Vehicle Trip",
			filters={"docstatus": DocStatus.submitted(),
			         "modified": ['between', [dt_start, dt_end]]},
			pluck="name",
		)

		for trip_name in trips:
			trip = frappe.get_doc("Passenger Vehicle Trip", trip_name)
			cond: str = trip.start_condition.strip().lower().replace(".", "")
			if cond != "ok":
				driver = frappe.db.get_value("Vehicle Driver", trip.driver, "driver_name")
				vah = frappe.db.get_value("Vaahan", trip.vaahan, "title")
				self.remarks.append(
					{"vaahan": vah, "driver": driver, "start_condition": trip.start_condition,
					 "remarks": trip.remarks})

	def get_subject(self):
		return self.email_template.get_formatted_subject({"date_of_report":self.date_of_report})

	def get_message(self):
		return self.email_template.get_formatted_response({"remarks": self.remarks})

	def load_recipients(self):
		self.email_to = frappe.get_doc("Vaahan Settings").maint_report_rcpt

	def send_email(self):

		email_args = {
			"recipients": self.email_to,
			"sender": None,
			"subject": self.get_subject(),
			"message": self.get_message(),
			"now": True,
		}
		#enqueue(method=frappe.sendmail, queue="short", timeout=300, is_async=True, **email_args)
		pprint(email_args)

	def update_last_run(self):
		settings = frappe.get_doc("Vaahan Settings")
		settings.trip_reported_till = self.date_of_report
		settings.save()

	def run_report(self):
		self.load_recipients()
		if not self.email_to:
			return

		self.load_trips()
		if self.remarks:
			self.send_email()
		self.update_last_run()

def daily():
	last_run = frappe.get_doc("Vaahan Settings").trip_reported_till
	day_next = add_to_date(last_run, days=1)

	if not last_run:
		last_run = "2024-01-01"
	yesterday = date.today() - timedelta(days=1)
	run_cnt = 0
	print(yesterday, day_next)
	while date_diff(yesterday, day_next) >= 0:
		print("running for ", day_next)
		email = PVTConditionEmail(day_next)
		email.run_report()
		day_next = add_to_date(day_next, days=1)
		run_cnt += 1
		if run_cnt > PVTConditionEmail.MAX_REPORT_RUNS_PER_DAY:
			break
