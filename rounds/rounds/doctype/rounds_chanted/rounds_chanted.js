// Copyright (c) 2016, Hemavatara dasa and contributors
// For license information, please see license.txt

frappe.ui.form.on('Rounds Chanted', {
	refresh: function(frm) {
        frm.add_custom_button(__("Update Balances"), function() {
            user = frm.doc.devotee;
            frappe.call({
				method: "rounds.rounds.doctype.rounds_chanted.rounds_chanted.update_balance",
				args: {
					"user": user
				},
				callback: function(r) {
					//frappe.model.sync(r.message);
					//frm.refresh();
					//console.log(user);
				}
			})
        });
	},
    beads: function(frm) {
        cur_frm.set_value("updated", true);
    },
    clicker: function(frm) {
        cur_frm.set_value("updated", true);
    },
    minimum_number: function(frm) {
        cur_frm.set_value("updated", true);
    }
});
