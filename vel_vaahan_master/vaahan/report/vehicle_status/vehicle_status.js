// Copyright (c) 2024, SMTW and contributors
// For license information, please see license.txt

frappe.query_reports["Vehicle Status"] = {
	filters: [
		{
			"fieldname": "model_group",
			"label": __("Model Group"),
			"fieldtype": "Link",
			"options": "Vehicle Model Group",
			"reqd": 1,
		},
	],
};
