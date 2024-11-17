// Copyright (c) 2024, SMTW and contributors
// For license information, please see license.txt

frappe.ui.form.on("Vehicle Refueling", {
	setup: function(frm) {
		frm.set_query("vaahan", "vehicle_details", function (doc) {
			return {
				query: "vel_vaahan_master.vaahan.doctype.vehicle_model.vehicle_model.vehicle_query",
				filters: {
					is_in_use: 1,
					fuel: doc.fuel_type,
				},
			};
		});
	}
});
