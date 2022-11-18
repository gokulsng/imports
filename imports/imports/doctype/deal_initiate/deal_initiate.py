# Copyright (c) 2021, Shivansh and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from num2words import num2words
from erpnext.setup.utils import get_exchange_rate

class DealInitiate(Document):
	def before_save(self):
		q=0
		a=0
		self.contact_email=frappe.db.get_value("Supplier",self.supplier,"email_id")
		c_currency=frappe.db.get_value("Company",{},"default_currency")
		self.conversion_rate=get_exchange_rate(self.currency,c_currency,self.date)
		for row in self.deal_initiate:
			#rate=frappe.db.get_value("Item Price",{"price_list":self.price_list},"price_list_rate")
			#row.amount=(row.qty*row.rate)
			#row.rate=row.rate
			#row.amount=(row.qty*row.rate)/self.conversion_rate
			q+=row.qty
			a+=row.amount
		self.total_quantity = q
		self.total_amount = a
		self.total_in_words = num2words(self.total_amount)

	def on_submit(self):
		df=frappe.new_doc("Deal Finalize")
		df.supplier=self.supplier
		df.currency=self.currency
		df.price_list=self.price_list
		df.deal_initiate=self.deal_initiate
		df.total_quantity=self.total_quantity
		df.total_in_words=self.total_in_words
		df.conversion_rate=self.conversion_rate
		df.total_amount=self.total_amount
		df.linked_deal=self.name
		df.save()
		#frappe.db.set_value("Deal Finalize",df.name,"assigned_to","anand@shyam-group.com")
		#df.save()
		dfn=frappe.db.get_value("Deal Finalize",{"linked_deal":self.name},"name")
#		frappe.errprint(type(dfn))
		link="/app/deal-finalize/"+dfn
		frappe.msgprint("Deal Finalize Created <a href="+link+">"+dfn+"</a>")

