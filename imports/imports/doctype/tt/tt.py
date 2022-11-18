# Copyright (c) 2022, Shivansh and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class TT(Document):
        def on_submit(self):
                doc=frappe.new_doc("ETD")
                val=self.items
                doc.supplier=self.supplier
                doc.currency=self.currency
                doc.price_list=self.price_list
                doc.schedule_date=self.schedule_date
                doc.company=self.company
                doc.transaction_date=self.transaction_date
                for row in val:
                        doc.append("items",{'item_code':row.item_code,'item_name':row.item_name,'uom':row.uom,'description':row.description,'rate':row.rate,'amount':row.amount,'qty':row.qty,'stock_uom':row.stock_uom,'payment_terms':row.payment_terms})
                doc.append("reference_payment_term",{'link_doctype':"TT",'link_name':self.name})
                doc.save()
                link="/app/etd/"+doc.name
                frappe.msgprint("ETD Created <a href="+link+">"+doc.name+"</a>")

