# Copyright (c) 2024, SMTW and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from datetime import date


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
			"label": "Driver",
			"fieldname": "driver",
			"fieldtype": "Link",
			"options":"Vehicle Driver",
		},
		{
			"label": "NT Valid Till",
			"fieldname": "valid_till_nt",
			"fieldtype": "Date",
		},
		{
			"label": "TR Valid Till",
			"fieldname": "valid_till_tr",
			"fieldtype": "Date",
		},
		{
			"label": "Status",
			"fieldname": "remarks",
			"fieldtype": "Data",
			"width": 250,
		},
		{
			"label": "License Type 2W",
			"fieldname": "license_type_2w",
			"fieldtype": "Data",
		},
		{
			"label": "License Type 4W",
			"fieldname": "license_type_4w",
			"fieldtype": "Data",
		},
	]


def get_data(filters) -> list[list]:
	"""Return data for the report.
	"""

	sql = """SELECT vd.title, vd.valid_till_nt, vd.valid_till_tr, '', vd.license_type_2w,
					vd.license_type_4w
				FROM `tabVehicle Driver` vd
				WHERE vd.is_active = 1
				ORDER BY LEAST(vd.valid_till_tr, vd.valid_till_nt) ASC;
				"""

	query_res = list(frappe.db.sql(sql))
	for i in range(len(query_res)):
		query_res[i] = list(query_res[i])
		if query_res[i][4] == "Not Applicable":
			query_res[i][4] = "-N/A-"
		if query_res[i][5] == "Not Applicable":
			query_res[i][5] = "-N/A-"
		if query_res[i][1] and query_res[i][2]:
			valid = (min(query_res[i][1], query_res[i][2]) - date.today()).days
			if valid < 0:
				remarks = "Expired"
			elif valid < 60:
				remarks = "Expiring in {} days".format(valid)
			else:
				remarks = ""
			query_res[i][3] = remarks
	return query_res
