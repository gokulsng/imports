# Copyright (c) 2022, Shivansh and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _

class LCUsance(Document):
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
		doc.append("reference_payment_term",{'link_doctype':"LC Usance",'link_name':self.name})
		doc.save()
		link="/app/etd/"+doc.name
		frappe.msgprint("ETD Created <a href="+link+">"+doc.name+"</a>")




	def before_save(self):
		link = "http://tpl.simpelerp.com"
		if self.workflow_state == "LC Draft To Be Receive & Upload":
			if not self.bank_account:
				frappe.throw("Bank Account is required")
			link1 = link + (self.lc_application_upload).replace(" ","%20")
			link2 = link + (self.indent).replace(" ","%20")
			link3 = link + (self.signed_po).replace(" ","%20")
			frappe.sendmail(recipients=[self.bank_email],sender="simpeltest2@gmail.com",message="<p>Open a PDF file for <a href = {0}>LC</a> <br> Open a PDF file for <a href = {1}>Indent</a> <br> Open a PDF file for <a href = {2}>PO</a> </p>".format(link1,link2,link3),
					subject=_('LC Application'))


		if self.workflow_state == "Awaiting Supplier Feedback":
			link1 = link + (self.lc_draft_upload_c).replace(" ","%20")
			frappe.sendmail(recipients=[self.contact_email],sender="simpeltest2@gmail.com",message="<p>Open a PDF file for <a href = {0}>LC</a> </p>".format(link1),
					subject=_('LC Draft'))


		if self.workflow_state == "Awaiting Acknowledge Copy":
			link1 = link + (self.supplier_correction_c).replace(" ","%20")
			frappe.sendmail(recipients=[self.bank_email],sender="simpeltest2@gmail.com",message="<p>Open a PDF file for <a href ={0}>LC</a></p>".format(link1),
					subject=_('LC Draft'))

		if self.workflow_state == "Awaiting For Supplier Feedback":
			l = len(self.amendment_c)
			if not l:
				link1 = link + (self.transmitted_copy_c).replace(" ","%20")
				frappe.sendmail(recipients=[self.contact_email],sender="simpeltest2@gmail.com",message="<p>Open a PDF file for <a href ={0}>Transmitted Copy</a></p>".format(link1),
						subject=_('LC Draft'))
			else:
				link1 = link + (self.amendment_c[l-1].swift_copy_c).replace(" ","%20")
				frappe.sendmail(recipients=[self.contact_email],sender="simpeltest2@gmail.com",message="<p>Open a PDF file for <a href ={0}>Swift Copy</a></p>".format(link1),
						subject=_('LC Draft'))


		if self.workflow_state == "Awaiting Swift Copy":
			l = len(self.amendment_c)
			link1 = link + (self.amendment_c[(l-1)].supplier_request_c).replace(" ","%20")
			frappe.sendmail(recipients=[self.bank_email],sender="simpeltest2@gmail.com",message="<p>Open a PDF file for <a href ={0}>Supplier Request</a></p>".format(link1),
					subject=_('LC Draft'))

@frappe.whitelist()
def get_bank_email(bank_name):
	p = frappe.db.get_value("Dynamic Link",{"link_doctype":"Bank Account","link_name":bank_name},"parent")
	doc = frappe.get_doc("Contact",p)
	return doc.email_id

