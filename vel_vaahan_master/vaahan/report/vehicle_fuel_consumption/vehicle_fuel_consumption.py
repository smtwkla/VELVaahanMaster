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
	"""
	return [
		{
			"label": _("Date"),
			"fieldname": "date",
			"fieldtype": "date",
		},
		{
			"label": _("Fuel Qty"),
			"fieldname": "fuel_qty",
			"fieldtype": "Int",
		},
		{
			"label": _("Odo"),
			"fieldname": "odo",
			"fieldtype": "Int",
		},
		{
			"label": _("Full"),
			"fieldname": "full",
			"fieldtype": "Check",
		},
		{
			"label": _("Supplier"),
			"fieldname": "fuel_supplier",
			"fieldtype": "Data",
		},
		{
			"label": _("Mileage"),
			"fieldname": "mileage",
			"fieldtype": "float",
		},

	]


def get_data(filters) -> list[list]:
	"""Return data for the report.
	"""

	vaahan = filters.get("vaahan")
	from_dt = filters.get("from_date")
	till_dt = filters.get("till_date")
	full_to_full = filters.get("full_to_full")

	from_sql = "AND vr.purchase_date>=%(from_date)s"
	till_sql = "AND vr.purchase_date<=%(till_date)s" if till_dt else ""

	sql = """SELECT vr.purchase_date, vrd.fuel_qty, vrd.odo, vrd.full_tank, vr.fuel_supplier, 0
				FROM `tabVehicle Refueling Details` vrd
				LEFT JOIN `tabVehicle Refueling` vr ON vrd.parent=vr.name
				WHERE vrd.vaahan = %(vaahan)s AND vr.docstatus = 1
				{from_sql} {till_sql}
				ORDER BY vr.purchase_date ASC""".format(vaahan=vaahan, from_sql=from_sql, till_sql=till_sql)

	query_res = list(frappe.db.sql(sql, filters))

	if full_to_full:
		if query_res:
			while not query_res[0][3]:
				del query_res[0]
		if query_res:
			while not query_res[-1][3]:
				del query_res[-1]

	tot_fuel = 0
	first_odo = last_odo = query_res[0][2] if query_res else 0
	for row in query_res:
		tot_fuel += row[1]
		last_odo = row[2]
	tot_km = last_odo - first_odo
	avg_mileage = round(tot_km / tot_fuel, 1) if tot_fuel else 0
	query_res = query_res + [("Total KM:", tot_fuel, tot_km, None, "Avg Kmpl:", avg_mileage, None, None),]

	return query_res
