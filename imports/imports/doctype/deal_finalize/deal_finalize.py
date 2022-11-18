# Copyright (c) 2021, Shivansh and contributors
# For license information, please see license.txt

import frappe,json
from frappe.model.document import Document
#from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

class DealFinalize(Document):
	def before_save(self):
		if self.saved:
			initial_item={}
			i_item=[]
			for row in self.deal_initiate:
				i_item.append(row.item_code)
				initial_item[row.item_code]=row.qty
			final_item={}
			f_item=[]
			for row in self.items:
				#row.amount=(row.qty*row.rate)
				#row.rate=row.rate/self.conversion_rate
				f_item.append(row.item_code)
				if row.item_code not in final_item:
					#frappe.throw("Item missing in table Deal Finalize " f'{row.item_code}')
					final_item[row.item_code]=[float(row.qty)]
				else:
					final_item[row.item_code].append(float(row.qty))
			if not f_item:
				frappe.throw("Deal Finalize Table is Empty")
			r_m_item=""
			for row in initial_item:
				if row not in final_item:
					r_item=float(initial_item[row])
					r_m_item+=(f'for item  "{row}"  :   Remaining Quantity - {r_item}<br>')
				#if not row in final_item:
				#	r_m_item+=(f'For Item  "{row}"  :   Remaining Quantity - {initial_item[row]}<br> Needs to be Filled')
				elif row in final_item and float(initial_item[row])!=float(sum(final_item[row])):
					frappe.errprint(i_item)
					frappe.errprint(f_item)
					r_item=float(initial_item[row])-float(sum(final_item[row]))
					r_m_item+=(f'for item  "{row}"  :   Remaining Quantity - {r_item}<br>')
			if r_m_item:
				frappe.throw("Total value is not matching,<br><br>" f'{r_m_item}')
		else:
			self.saved=1
	def before_submit(self):
		self.before_save()

@frappe.whitelist()
def get_rate(item,dn):
	rate=frappe.db.get_value("Deal Initiate Item",{"parent":dn,"item_code":item},"rate")
	#frappe.errprint(rate)
	return rate



@frappe.whitelist()
def make_indent(val,supplier,date,currency,price_list,name):
	val=json.loads(val)
#	frappe.errprint(val)
	if not val:
		frappe.throw("No rows selected")
	p_details={}
	#frappe.errprint(val)
	#for row in val:
	#	if row["payment_terms"] == "LC @ Sight":
	#		row["payment_terms"]="LC"
	#frappe.errprint(val)
	for row in val:
		if row["payment_terms"] not in p_details:
			p_details[row['payment_terms']]=[row["buyer"]]
		elif row['buyer'] not in p_details[row['payment_terms']]:
			p_details[row['payment_terms']].append(row["buyer"])
			#p_term=row['payment_terms']
			#frappe.throw("Buyer not matching for "f'{p_term}')
	#frappe.errprint(p_details)
	r_m_buyer=""
	for row in p_details:
		if(len(set(p_details[row]))>1):
			r_m_buyer+=(f'{row}<br>')
	if r_m_buyer:
		frappe.throw("Buyer's not matching for Payment Terms<br><br>" f'{r_m_buyer}')
	else:
		for a_row in p_details:
			#frappe.errprint("in")
			doc=frappe.new_doc("Purchase Order")
			doc.supplier=supplier
			doc.schedule_date=date
		#	frappe.errprint(currency)
		#	frappe.errprint(price_list)
			doc.currency=currency
			doc.buying_price_list=price_list
			flag = 0
			Count = 0
			for row in val:
				if row["payment_terms"] == a_row and row['indent'] == 0:
					flag = 1
					Count+=1
					df = frappe.get_doc("Deal Finalize",name)
					df.items[(row['idx']-1)].indent = 1
					df.save()
					if not doc.company == row["buyer"]:
						doc.company=row['buyer']
						w=frappe.db.get_value("Warehouse",{"warehouse_name":"Stores","company":row['buyer']},"name")
						doc.set_warehouse=w
					doc.append("items",{'item_code':row['item_code'],'item_name':row['item_name'],'uom':row['uom'],'description':row['description'],'rate':row['rate'],'amount':row['amount'],'qty':row['qty'],'stock_uom':row['stock_uom'],'payment_terms':row['payment_terms'],'palletized':row['palletized'],'port':row['port'],'country_of_origin':row['country_of_origin'],'incoterms':row['incoterms'],'buyer':row['buyer']})
			if flag:
				doc.linked_deal_finalize=name
				doc.save()
				flag = 0
		if Count:
			frappe.msgprint("Indent Created")
		else:
			frappe.msgprint('Indent Already Created for the selected record')

@frappe.whitelist()
def make_payment_terms(self,method):
	if (self.items[0].payment_terms == "DA"):
		doc=frappe.new_doc("DA")
		val=self.items
		doc.supplier=self.supplier
		doc.currency=self.currency
		doc.price_list=self.buying_price_list
		doc.schedule_date=self.schedule_date
		doc.company=self.company
		doc.transaction_date=self.transaction_date
		for row in val:
			doc.append("items",{'item_code':row.item_code,'item_name':row.item_name,'uom':row.uom,'description':row.description,'rate':row.rate,'amount':row.amount,'qty':row.qty,'stock_uom':row.stock_uom,'payment_terms':row.payment_terms})
		doc.linked_indent=self.name
		doc.total_quantity=self.total_qty
		doc.total_in_words=self.in_words
		doc.total_amount=self.total
		doc.save()
		link="/app/da/"+doc.name
		frappe.msgprint("DA Created <a href="+link+">"+doc.name+"</a>")

	if (self.items[0].payment_terms == "LC @ Sight"):
		doc=frappe.new_doc("LC")
		val=self.items
		doc.supplier=self.supplier
		doc.indent_no_c = self.indent_no_c
		doc.company=self.company
		doc.currency=self.currency
		doc.price_list=self.buying_price_list
		doc.schedule_date=self.schedule_date
		doc.transaction_date=self.transaction_date
		for row in val:
			doc.append("items",{'item_code':row.item_code,'item_name':row.item_name,'uom':row.uom,'description':row.description,'rate':row.rate,'amount':row.amount,'qty':row.qty,'stock_uom':row.stock_uom,'payment_terms':row.payment_terms})
		doc.linked_indent=self.name
		doc.total_quantity=self.total_qty
		doc.total_in_words=self.in_words
		doc.total_amount=self.total
		doc.save()
		link="/app/lc/"+doc.name
		frappe.msgprint("LC Created <a href="+link+">"+doc.name+"</a>")

	if (self.items[0].payment_terms == "TT + DP"):
		doc=frappe.new_doc("TT DP")
		val=self.items
		doc.supplier=self.supplier
		doc.company=self.company
		doc.transaction_date=self.transaction_date
		doc.schedule_date=self.schedule_date
		doc.currency=self.currency
		doc.price_list=self.buying_price_list
		for row in val:
			doc.append("items",{'item_code':row.item_code,'item_name':row.item_name,'uom':row.uom,'description':row.description,'rate':row.rate,'amount':row.amount,'qty':row.qty,'stock_uom':row.stock_uom,'payment_terms':row.payment_terms,'hsnsac':row.gst_hsn_code})
		doc.linked_indent=self.name
		doc.total_quantity=self.total_qty
		doc.total_in_words=self.in_words
		doc.total_amount=self.total
		doc.save()
		link="/app/tt-dp/"+doc.name
		frappe.msgprint("TT DP Created <a href="+link+">"+doc.name+"</a>")

	if (self.items[0].payment_terms == "LC Usance"):
		doc=frappe.new_doc("LC Usance")
		val=self.items
		doc.supplier=self.supplier
		doc.company=self.company
		doc.transaction_date=self.transaction_date
		doc.schedule_date=self.schedule_date
		doc.currency=self.currency
		doc.price_list=self.buying_price_list
		for row in val:
			doc.append("items",{'item_code':row.item_code,'item_name':row.item_name,'uom':row.uom,'description':row.description,'rate':row.rate,'amount':row.amount,'qty':row.qty,'stock_uom':row.stock_uom,'payment_terms':row.payment_terms})
		doc.linked_indent=self.name
		doc.total_quantity=self.total_qty
		doc.total_in_words=self.in_words
		doc.total_amount=self.total
		doc.save()
		link="/app/lc-usance/"+doc.name
		frappe.msgprint("LC Usance Created <a href="+link+">"+doc.name+"</a>")


