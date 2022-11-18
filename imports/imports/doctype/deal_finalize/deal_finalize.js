// Copyright (c) 2021, Shivansh and contributors
// For license information, please see license.txt

frappe.ui.form.on('Deal Finalize', {
	refresh: function(frm) {
		if(frm.doc.docstatus===1){
//			console.log("in")
//			const val=cur_frm.fields_dict.items.grid.get_selected_children()
			frm.add_custom_button(__('Attach Indent'), function() {
				frm.events.create_indent(frm)
			});
		}
	},
	 create_indent:function(frm)
        {
            frappe.call
            ({
                method:
                "imports.imports.doctype.deal_finalize.deal_finalize.make_indent",
                args: 
                {
                    date:frm.doc.date,
                    supplier:frm.doc.supplier,
                    val: cur_frm.fields_dict.items.grid.get_selected_children(),
                    currency:frm.doc.currency,
                    price_list:frm.doc.price_list,
                    name:frm.doc.name
                },
                callback: function (r) 
                {
                },
            });
        }
});
frappe.ui.form.on('Deal Finalize Item', {
        // refresh: function(frm) {

        // }
	item_code: function(frm,cdt,cdn) {
		//console.log("in")
		const d=locals[cdt][cdn]
		frappe.call({
			method:"imports.imports.doctype.deal_finalize.deal_finalize.get_rate",
			args:{
				dn:frm.doc.linked_deal,
				item:d.item_code
			},
			callback :function(r){
		//		console.log(r)
				if(r){
					frappe.model.set_value(cdt,cdn,"rate",r.message);
				}
			}
		});

        },
        qty:function(frm,cdt,cdn) {
                const d=locals[cdt][cdn]
                frappe.model.set_value(cdt,cdn,"amount",d.rate*d.qty);
        },
	rate: function(frm,cdt,cdn){
		const d=locals[cdt][cdn]
		frappe.model.set_value(cdt,cdn,"amount",d.rate*d.qty);
	}
});
