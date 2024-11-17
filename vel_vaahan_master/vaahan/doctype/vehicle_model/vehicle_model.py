# Copyright (c) 2024, SMTW and contributors
# For license information, please see license.txt
from tabnanny import check

import json

import frappe
from frappe.model.document import Document


class VehicleModel(Document):
	def before_save(self):
		self.payload = self.gvw - self.uvw

	def check_weights(self):
		if self.gvw < self.uvw:
			frappe.throw("Vehicle gross weight cannot be lesser than unladen weight.")

	def check_tyre_config(self):
		tyre_pos = [t.tyre_position for t in self.tyres]
		if len(tyre_pos) != len(set(tyre_pos)):
			frappe.throw("Vehicle tyre position contains duplicates. Must be unique.")
		pos_count = len([i.name for i in self.tyres if i.tyre_position != 'Stepney'])
		if pos_count != self.number_of_tyres and len(tyre_pos) != 0:
			frappe.throw("Vehicle's number of tyres is {} but table contains {} tyres.".format(
						self.number_of_tyres, pos_count))

	def validate(self):
		self.check_weights()
		self.check_tyre_config()

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def vehicle_query(doctype, txt, searchfield, start, page_len, filters, as_dict=False):
	if isinstance(filters, str):
		filters = json.loads(filters)

	conjunction = ""
	in_use = ""
	if "is_in_use" in filters:
		in_use = "is_in_use={}".format(filters.get("is_in_use"))
		conjunction = " AND "

	is_gv = ""
	if "is_gv" in filters:
		is_gv = conjunction + "vm.is_gv={}".format(filters.get("is_gv"))
		conjunction = " AND "

	fuel_is = ""
	if "fuel" in filters:
		fuel_is = conjunction + "vm.fuel='{}'".format(filters.get("fuel"))

	where = " WHERE " if (in_use or is_gv) else ""
	sql = """
	SELECT v.name FROM tabVaahan v LEFT JOIN `tabVehicle Model` vm ON v.model = vm.name
		{where} {in_use}
		{is_gv}
		{fuel_is};
		""".format(where=where,in_use=in_use, is_gv=is_gv, fuel_is=fuel_is)
	print(sql)
	return frappe.db.sql(sql,{},as_dict=as_dict)
