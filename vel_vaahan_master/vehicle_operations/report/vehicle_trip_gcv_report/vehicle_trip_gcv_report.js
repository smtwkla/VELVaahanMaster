// Copyright (c) 2024, SMTW and contributors
// For license information, please see license.txt

frappe.query_reports["Vehicle Trip GCV Report"] = {
filters: [
		{
			fieldname: "vaahan",
			"label": __("Vaahan"),
			"fieldtype": "Link",
			"reqd": 0,
			"options": "Vaahan"
		},
		{
			fieldname: "vehicle_model",
			"label": __("Vehicle Model"),
			"fieldtype": "Link",
			"reqd": 0,
			"options": "Vehicle Model"
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
	],
};
