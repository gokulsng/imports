// Copyright (c) 2022, Shivansh and contributors
// For license information, please see license.txt

frappe.ui.form.on('LC', {
	bank_account: function(frm) {
		if(frm.doc.bank_account){
			frappe.call({
			method: 'imports.imports.doctype.lc.lc.get_bank_email',
			args: {
				'bank_name': frm.doc.bank_account
			},
			callback: function(r) {
				if (r.message) {
					console.log(r.message)
					frm.set_value("bank_email",r.message)
				}
			}
			})
		}
	}
});
