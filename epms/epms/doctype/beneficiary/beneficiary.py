# Copyright (c) 2023, Management System for Agrasarteach@suvaidyam.com and contributors
# For license information, please see license.txt

import frappe
import json
from frappe.model.document import Document

class Beneficiary(Document):

	def after_insert(self):
		beneficiary = frappe.get_doc("Beneficiary" , self.name)
		if(beneficiary.are_you_parents == 1):
			family_doc = frappe.new_doc("Family")
			family_doc.head_of_family = beneficiary.name
			family_doc.name_of_parents = beneficiary.name_of_the_beneficiary
			family_doc.name_of_parents = beneficiary.contact_number
			family_doc.insert()
		else:
			print("CREATING CHILD BENEFICARY")

	def after_insert(self):
		print("hello")

