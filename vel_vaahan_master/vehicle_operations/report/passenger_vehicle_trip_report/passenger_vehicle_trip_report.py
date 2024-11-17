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
			"fieldname": "pt",
			"label": "ID",
			"fieldtype": "Link",
			"options": "Passenger Vehicle Trip",
		},
		{
			"fieldname": "vaahan",
			"label": "Vaahan",
			"fieldtype": "Link",
			"options": "Vaahan",
		},
		{
			"fieldname": "driver",
			"label": "Driver",
			"fieldtype": "Link",
			"options": "Vehicle Driver",
		},
		{
			"fieldname": "start_datetime",
			"label": "Start",
			"fieldtype": "Date",
		},
		{
			"fieldname": "km",
			"label": "KM",
			"fieldtype": "Int",
		},
		{
			"fieldname": "Time",
			"label": "Time",
			"fieldtype": "Float",
		},
	]


def get_data(filters) -> list[list]:
	"""Return data for the report.	"""

	vaahan = filters.get("vaahan")
	vehicle_model = filters.get("vehicle_model")
	from_dt = filters.get("from_date")
	till_dt = filters.get("till_date")

	if vehicle_model:
		v_list = frappe.db.get_list("Vaahan", filters={'model':vehicle_model}, pluck='name')
		v_list_str = ""
		for v in v_list:
			v_list_str += f"'{v}',"
		vm_sql = "AND pt.vaahan IN ({})".format(v_list_str[:-1])
	else:
		vm_sql = ""

	vaahan_sql = "AND pt.vaahan='{}'".format(vaahan) if vaahan else ""
	from_sql = "AND pt.start_datetime>='{}'".format(from_dt)
	till_sql = "AND pt.start_datetime<='{}'".format(till_dt) if till_dt else ""

	sql = """SELECT pt.name, pt.vaahan, pt.driver, pt.start_datetime, pt.total_km, pt.total_time
				FROM `tabPassenger Vehicle Trip` pt
				WHERE pt.docstatus = 1 {vaahan_sql} {vm_sql}
				{from_sql} {till_sql}
				ORDER BY pt.start_datetime ASC""".format(vaahan_sql=vaahan_sql, from_sql=from_sql,
	                                                     till_sql=till_sql, vm_sql=vm_sql)

	query_res = list(frappe.db.sql(sql))

	total_km = total_time = 0
	for row in query_res:
		total_km += row[4]
		total_time += row[5]
	query_res = query_res + [[None,None,None,"Totals:", total_km, total_time],]

	return query_res
