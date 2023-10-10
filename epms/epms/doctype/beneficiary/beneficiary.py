# Copyright (c) 2023, Management System for Agrasarteach@suvaidyam.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from epms.utils.cache import Cache

class Beneficiary(Document):
	def after_insert(self):
		# if other select then auto add in list next time
		if(self.new_occupation):
			new_occupation_doc = frappe.new_doc("Current Occupation")
			new_occupation_doc.occupation = self.new_occupation
			new_occupation_doc.save()
		if(self.other_bank_account):
			new_bank_doc = frappe.new_doc("Bank")
			new_bank_doc.bank_name = self.other_bank_account
			new_bank_doc.save()
		if(self.other_current_location):
			new_location_doc = frappe.new_doc("Current location")
			new_location_doc.name_of_location = self.other_current_location
			new_location_doc.save()
		# if(self.other_caste_category):
		# 	new_cast_category = frappe.new_doc("Caste master")
		# 	new_cast_category.caste = self.other_caste_category
		# 	new_cast_category.save()
		# if(self.other_source_information_about_center):
		# 	new_source = frappe.new_doc("Source information about center")
		# 	new_source.source_information_about_center = self.other_source_information_about_center
		# 	new_source.save()

		beneficiary = frappe.get_doc("Beneficiary" , self.name)
		# csc_id = frappe.cache().get_value("csc-"+(frappe.session.user))
		beneficiary.csc = Cache.get_csc()
		if(self.head_of_family == "No"):
			family_doc = frappe.new_doc("Primary Member")
			family_doc.head_of_family = beneficiary.name
			family_doc.name_of_parents = beneficiary.name_of_the_beneficiary
			family_doc.contact_number = beneficiary.contact_number
			family_doc.csc = beneficiary.csc
			family_doc.insert()
			# update current beneficery
			beneficiary.family = family_doc.name
			beneficiary.save()
		else:
			print("CREATING CHILD BENEFICARY")
	
	def on_update(self):
		beneficiary = frappe.get_doc("Beneficiary" , self.name)
		# csc_id = frappe.cache().get_value("csc-"+(frappe.session.user))
		# beneficiary.csc = Cache.get_csc()
		if(self.head_of_family == "No"):
			family_doc_name = frappe.get_list("Primary Member",
        	filters={'head_of_family': beneficiary.name},
        	fields=["name"])
			if(family_doc_name):
				family_doc = frappe.get_doc("Primary Member", family_doc_name[0].name)
				family_doc.name_of_parents = beneficiary.name_of_the_beneficiary
				family_doc.contact_number = beneficiary.contact_number
				# family_doc.csc = beneficiary.csc
				family_doc.save()
			else:
				family_doc = frappe.new_doc("Primary Member")
				family_doc.head_of_family = beneficiary.name
				family_doc.name_of_parents = beneficiary.name_of_the_beneficiary
				family_doc.contact_number = beneficiary.contact_number
				family_doc.csc = beneficiary.csc
				family_doc.insert()
				# update current beneficery to family
				beneficiary.family = family_doc.name
				beneficiary.save()
				frappe.msgprint("New Beneficary Update As a Head of Family")
		else:
			print("THis is beneficary is not a parent ")