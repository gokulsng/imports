// Copyright (c) 2021, Shivansh and contributors
// For license information, please see license.txt

//frappe.ui.form.on('Deal Initiate', {
//	refresh: function(frm) {
//		if(frm.doc.docstatus == 1 ) {
//			frm.add_custom_button(__('Create Deal Finalize'), () =>{
//			frm.trigger("make_deal_finalize");
//		},__('Create'));
//		}
//	},
//	make_deal_finalize: function(frm) {
//	frappe.model.open_mapped_doc({
//	method: "imports.imports.doctype.deal_finalize.deal_finalize.make_deal_finalize",
//	frm: frm
//	})
//	}
//});
frappe.ui.form.on('Deal Initiate Item', {
//	validate: function(frm) {

	//}
	item_code: function(frm,cdt,cdn) {
//		console.log("inn")
		const d=locals[cdt][cdn]
		frappe.db.get_value("Item Price",{"item_code":d.item_code,'price_list':frm.doc.price_list},'price_list_rate', (r) => {
			if (r.price_list_rate) {
				frappe.model.set_value(cdt,cdn,"amount",r.price_list_rate);
				frappe.model.set_value(cdt,cdn,"rate",r.price_list_rate);
			}
		});
	},
	qty: function(frm,cdt,cdn) {
		const d=locals[cdt][cdn]
		frappe.model.set_value(cdt,cdn,"amount",d.rate*d.qty);
	},
	rate: function(frm,cdt,cdn){
		const d=locals[cdt][cdn]
		frappe.model.set_value(cdt,cdn,"amount",d.rate*d.qty);
	}
});
