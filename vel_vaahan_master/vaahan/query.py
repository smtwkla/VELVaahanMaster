import frappe
import json


@frappe.whitelist()
def vaahan_tyre_pos(doctype=None, txt=None, searchfield=None, start=None, page_len=None, filters=None, as_dict=False):
	if isinstance(filters, str):
		filters = json.loads(filters)
	print("called")
	if not filters or "vaahan" not in filters:
		return None
	v = frappe.get_doc('Vaahan', filters.get("vaahan"))
	vm = frappe.get_doc('Vehicle Model', v.model)
	tyres = [(t.tyre_position,) for t in vm.tyres]
	return tyres


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def vaahan_list_query(doctype, txt, searchfield, start, page_len, filters, as_dict=False):
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
	res = frappe.db.sql(sql,{},as_dict=as_dict)
	return res
