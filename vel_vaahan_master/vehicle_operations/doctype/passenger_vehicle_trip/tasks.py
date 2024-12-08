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

	@staticmethod
	def condition_text_present(txt):
		return txt.strip().lower().replace(".", "") != "ok"

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
			if (self.condition_text_present(trip.start_condition) or
					self.condition_text_present(trip.end_condition)):
				driver = frappe.db.get_value("Vehicle Driver", trip.driver, "driver_name")
				vah = frappe.db.get_value("Vaahan", trip.vaahan, "title")
				self.remarks.append(
					{"vaahan": vah, "driver": driver, "start_condition": trip.start_condition,
					 "end_condition": trip.end_condition})

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
		enqueue(method=frappe.sendmail, queue="short", timeout=300, is_async=True, **email_args)


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

	if not last_run:
		last_run = "2024-01-01"
	day_next = add_to_date(last_run, days=1)

	yesterday = date.today() - timedelta(days=1)
	run_cnt = 0
	while date_diff(yesterday, day_next) >= 0:
		email = PVTConditionEmail(day_next)
		email.run_report()
		day_next = add_to_date(day_next, days=1)
		run_cnt += 1
		if run_cnt > PVTConditionEmail.MAX_REPORT_RUNS_PER_DAY:
			break

def create_pv_trip_condition_email_template():
	template = None
	if not frappe.db.exists("Email Template", PVTConditionEmail.PV_TRIP_CONDITION_TEMPLATE):
		template = frappe.get_doc(
			{
				"doctype": "Email Template",
				"name": PVTConditionEmail.PV_TRIP_CONDITION_TEMPLATE,
				"use_html": True,
				"subject": "Passenger Vehicle Condition Feedback - {{ date_of_report }}",
				"response_html": """
<table>
    <tr>
        <th>Sl.</th>
        <th>Vaahan</th>
        <th>Driver</th>
        <th>Start Condition</th>
        <th>End Condition</th>
    </tr>

{% for item in remarks %}
    <tr>
        <td>{{ item.vaahan }}</td>
        <td>{{ item.driver }}</td>
        <td>{{ item.start_condition }}</td>
        <td>{{ item.end_condition }}</td>
    </tr>
{% endfor %}
</table>
""",
			}
		)
		template.insert()

def execute():
	create_pv_trip_condition_email_template()
