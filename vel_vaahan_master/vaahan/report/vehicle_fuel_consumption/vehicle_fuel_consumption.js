// Copyright (c) 2024, SMTW and contributors
// For license information, please see license.txt

frappe.query_reports["Vehicle Fuel Consumption"] = {
	filters: [
		{
			fieldname: "vaahan",
			"label": __("Vaahan"),
			"fieldtype": "Link",
			"reqd": 1,
			"options": "Vaahan"
		},
		{
			fieldname: "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"reqd": 1
		},
		{
			fieldname: "till_date",
			"label": __("Till Date"),
			"fieldtype": "Date",
			"reqd": 0
		},
		{
			fieldname: "full_to_full",
			"label": __("Full to Full"),
			"fieldtype": "Check",
			"reqd": 0
		},
	],
};
