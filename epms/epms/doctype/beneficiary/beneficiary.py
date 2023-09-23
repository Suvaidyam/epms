# Copyright (c) 2023, Management System for Agrasarteach@suvaidyam.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Beneficiary(Document):
	global no_of_overall_status
	def after_insert(self):
		beneficiary = frappe.get_doc("Beneficiary" , self.name)
		if(self.head_of_family == 1):
			family_doc = frappe.new_doc("Family")
			family_doc.head_of_family = beneficiary.name
			family_doc.name_of_parents = beneficiary.name_of_the_beneficiary
			family_doc.contact_number = beneficiary.contact_number
			family_doc.insert()
			# update current beneficery
			beneficiary.family = family_doc.name
			beneficiary.save()
		else:
			print("CREATING CHILD BENEFICARY")
	
	def on_update(self):
		beneficiary = frappe.get_doc("Beneficiary" , self.name)
		if(self.head_of_family == 1):
			family_doc_name = frappe.get_list("Family",
        	filters={'head_of_family': beneficiary.name},
        	fields=["name"])
			if(family_doc_name):
				family_doc = frappe.get_doc("Family", family_doc_name[0].name)
				family_doc.name_of_parents = beneficiary.name_of_the_beneficiary
				family_doc.contact_number = beneficiary.contact_number
				family_doc.save()
			else:
				family_doc = frappe.new_doc("Family")
				family_doc.head_of_family = beneficiary.name
				family_doc.name_of_parents = beneficiary.name_of_the_beneficiary
				family_doc.contact_number = beneficiary.contact_number
				family_doc.insert()
				# update current beneficery to family
				beneficiary.family = family_doc.name
				beneficiary.save()	
				frappe.msgprint("New Beneficary Update As a Head of Family")
		else:
			print("THis is beneficary is not a parent ")
