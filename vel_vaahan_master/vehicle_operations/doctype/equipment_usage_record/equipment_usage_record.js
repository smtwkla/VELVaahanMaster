// Copyright (c) 2024, SMTW and contributors
// For license information, please see license.txt

frappe.ui.form.on("Equipment Usage Record", {
	setup: function(frm) {
		frm.set_query("driver", function() {
			return {
				filters: {
					is_active: 1,
				},
			};
		});
		frm.set_query("vaahan", function() {
			return {
				query: "vel_vaahan_master.vaahan.query.vaahan_list_query",
				filters: {
					is_in_use: 1,
					odometer: 'Hour Meter',
				},
			};
		});
		frm.set_query("route", function() {
			return {
				filters: {
					in_use: 1,
					docstatus: 1,
				},
			};
		});
	}
});
