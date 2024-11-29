# Copyright (c) 2024, SMTW and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters: dict | None = None):
	"""Return columns and data for the report.

	This is the main entry point for the report. It accepts the filters as a
	dictionary and should return columns and data. It is called by the framework
	every time the report is refreshed or a filter is updated.
	"""
	columns = get_columns()
	data = get_data(filters)

	return columns, data


def get_columns() -> list[dict]:
	"""Return columns for the report.

	One field definition per column, just like a DocType field definition.
	"""
	return [
		{
			"label": _("Model"),
			"fieldname": "model",
			"fieldtype": "Data",
			"width": 150,
		},
		{
			"label": _("RegNo"),
			"fieldname": "registration",
			"fieldtype": "Int",
		},
		{
			"label": _("Mfr"),
			"fieldname": "mfr",
			"fieldtype": "Data",
			"width": 85,
		},
		{
			"label": _("Payload"),
			"fieldname": "payload",
			"fieldtype": "Int",
		},
		{
			"label": _("Status"),
			"fieldname": "status",
			"fieldtype": "Data",
		},
		{
			"label": _("FC"),
			"fieldname": "fc_valid_till",
			"fieldtype": "Date",
			"width": 120,
		},
		{
			"label": _("Insurance"),
			"fieldname": "insurance_valid_till",
			"fieldtype": "Date",
			"width": 120,
		},
		{
			"label": _("PUC"),
			"fieldname": "puc_valid_till",
			"fieldtype": "Date",
			"width": 120,
		},
		{
			"label": _("Road Tax"),
			"fieldname": "road_tax_valid_till",
			"fieldtype": "Date",
			"width": 120,
		},
		{
			"label": _("Green Tax"),
			"fieldname": "green_tax_valid_till",
			"fieldtype": "Date",
			"width": 120,
		},
		{
			"label": _("Permit"),
			"fieldname": "permit_valid_till",
			"fieldtype": "Date",
			"width": 120,
		},
	]


def get_data(filters) -> list[list]:
	"""Return data for the report.

	The report data is a list of rows, with each row being a list of cell values.
	"""

	mg = filters.get("model_group")
	print(mg)
	csql = """
	SELECT vm.model as model, v.registration as registration, v.manufacture_mon_yr as mfr,
			vm.payload as payload, v.status as status, v.fc_valid_till as fc_valid_till, v.insurance_valid_till as insurance_valid_till,
			v.permit_valid_till as permit_valid_till, v.road_tax_valid_till as road_tax_valid_till,
			v.green_tax_valid_till as green_tax_valid_till, v.puc_valid_till as puc_valid_till
	FROM `tabVaahan` v LEFT JOIN `tabVehicle Model` vm ON (v.model = vm.name)
	WHERE vm.model_group = '{mg}'
	ORDER BY LEAST(v.green_tax_valid_till, v.puc_valid_till, v.permit_valid_till, v.road_tax_valid_till,
			v.fc_valid_till, v.insurance_valid_till);
	""".format(mg=mg)

	query_res = frappe.db.sql(csql, as_dict=True)
	return query_res
