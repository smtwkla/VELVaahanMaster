# Copyright (c) 2024, SMTW and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from datetime import date
#import pandas as pd


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
			"label": "ID",
			"fieldname": "name",
			"fieldtype": "Link",
			"options":"Vehicle Driver",
		},
		{
			"label": "Driver",
			"fieldname": "driver_name",
			"fieldtype": "Data",
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
			"fieldname": "status",
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

	# query_res = list(frappe.db.sql(sql))

	query_res = frappe.db.get_list("Vehicle Driver", filters={"is_active":1},
	                               fields=["name", "driver_name", "valid_till_nt", "valid_till_tr",
	                                       "license_type_2w", "license_type_4w"])
	# df = pd.Dataframe.from_records(query_res)

	def check_valid(row):
		if row["valid_till_nt"] and row["valid_till_tr"]:
			recent_exp = min(row["valid_till_nt"], row["valid_till_tr"])
		else:
			recent_exp = row["valid_till_nt"] or row["valid_till_tr"]
		expiring_in = (recent_exp - date.today()).days
		if expiring_in < 0:
			return "Expired"
		elif expiring_in < 60:
			return "Expiring in {} days".format(expiring_in)
		else:
			return ""

		return expiring_in

	for r in query_res:
		r["status"] = check_valid(r)
		if r["license_type_2w"] == "Not Applicable":
			r["license_type_2w"] = "N/A"
		if r["license_type_4w"] == "Not Applicable":
			r["license_type_4w"] = "N/A"
		if not r["valid_till_tr"]:
			print(r)
	query_res.sort(key=lambda x: min(x["valid_till_nt"],x["valid_till_tr"]) \
								if x["valid_till_nt"] and x["valid_till_tr"] \
								else x["valid_till_nt"] or x["valid_till_tr"])
	return query_res
