import frappe


def execute():
	if frappe.db.has_column('Vehicle Driver', 'gen_title'):
		frappe.db.sql("""
			UPDATE `tabVehicle Driver` vd SET vd.title = vd.gen_title
				WHERE vd.title is NULL;
		""")
		frappe.db.sql_ddl("""
			ALTER TABLE `tabVehicle Driver` DROP COLUMN gen_title;
		""")
