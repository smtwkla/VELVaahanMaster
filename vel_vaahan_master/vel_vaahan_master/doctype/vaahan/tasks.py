import frappe


def daily():
	all_vehicles = frappe.get_list('Vaahan', pluck='name')
	for v in all_vehicles:
		frappe.get_doc('Vaahan', v).run_daily_scheduled_tasks()
