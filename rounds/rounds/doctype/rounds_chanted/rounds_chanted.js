// Copyright (c) 2016, Hemavatara dasa and contributors
// For license information, please see license.txt

frappe.ui.form.on('Rounds Chanted', {
	refresh: function(frm) {
        frm.add_custom_button(__("Update Balances"), function() {
            //console.log(frm.doc.devotee);
            frappe.call({
				method: "rounds.rounds.doctype.rounds_chanted.rounds_chanted.update_balance",
				args: {
					"user": frm.doc.devotee
				},
				callback: function(r) {
					//frappe.model.sync(r.message);
					//frm.refresh();
					frappe.msgprint("Done");
				},
				freeze: true,
				freeze_message: 'Calculating Balances....'
			})
        });
	},
    beads: function(frm) {
        cur_frm.set_value("updated", true);
        cur_frm.set_value("start_here", false);
    },
    clicker: function(frm) {
        cur_frm.set_value("updated", true);
        cur_frm.set_value("start_here", false);
    },
    minimum_number: function(frm) {
        cur_frm.set_value("updated", true);
        cur_frm.set_value("start_here", false);
    }
});
