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
	return [
		{
			"label": _("VT"),
			"fieldname": "vehicle_trip",
			"fieldtype": "Link",
			"options": "Vehicle Trip GCV",
		},
		{
			"label": _("Vaahan"),
			"fieldname": "vaahan",
			"fieldtype": "Link",
			"options": "Vaahan",
		},
		{
			"label": _("Trip Date"),
			"fieldname": "trip_date",
			"fieldtype": "Date",
		},
		{
			"label": _("KM"),
			"fieldname": "km",
			"fieldtype": "Int",
		},
		{
			"label": _("Freight"),
			"fieldname": "freight",
			"fieldtype": "Currency",
		},
	]


def get_data(filters) -> list[list]:

	vaahan = filters.get("vaahan")
	vehicle_model = filters.get("vehicle_model")
	from_dt = filters.get("from_date")
	till_dt = filters.get("till_date")

	if vehicle_model:
		v_list = frappe.db.get_list("Vaahan", filters={'model':vehicle_model}, pluck='name')
		v_list_str = ""
		for v in v_list:
			v_list_str += f"'{v}',"
		vm_sql = "AND vt.vaahan IN ({})".format(v_list_str[:-1])
	else:
		vm_sql = ""

	vaahan_sql = "AND vt.vaahan='{}'".format(vaahan) if vaahan else ""
	from_sql = "AND vt.start_datetime>='{}'".format(from_dt)
	till_sql = "AND vt.start_datetime<='{}'".format(till_dt) if till_dt else ""

	sql = """SELECT vt.name, vt.vaahan, vt.start_datetime, vt.total_km, vt.total_freight
				FROM `tabVehicle Trip GCV` vt
				WHERE vt.docstatus = 1 {vaahan_sql} {vm_sql}
				{from_sql} {till_sql}
				ORDER BY vt.start_datetime ASC""".format(vaahan_sql=vaahan_sql, from_sql=from_sql,
	                                                     till_sql=till_sql, vm_sql=vm_sql)

	query_res = list(frappe.db.sql(sql))

	total_km = total_freight = 0
	for row in query_res:
		total_km += row[3]
		total_freight += row[4]

	query_res = query_res + [[None,None,"Totals:", total_km, total_freight],]

	return query_res
