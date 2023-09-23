# Copyright (c) 2023, Management System for Agrasarteach@suvaidyam.com and contributors
# For license information, please see license.txt

import frappe
import json
from frappe.model.document import Document

class Beneficiary(Document):
	global no_of_overall_status
	def after_insert(self):
		# beneficiary = frappe.get_doc("Beneficiary" , self.name)
		if(self.head_of_family == 1):
			family_doc = frappe.new_doc("Family")
			family_doc.head_of_family = self.name
			family_doc.name_of_parents = self.name_of_the_beneficiary
			family_doc.contact_number = self.contact_number
			family_doc.insert()
			# update current beneficery
			self.family = family_doc.name
			# self.save()
		else:
			print("CREATING CHILD BENEFICARY")
	
	def on_update(self):
		# beneficiary = frappe.get_doc("Beneficiary" , self.name)
		# status_under_process = 0
		# status_open = 0
		# status_form_submitted = 0
		# status_rejected = 0
		# status_completed = 0
		# if(self.support_table):
			# for item in self.support_table:
			# 	if(item.status == 'Open'):
			# 		status_open += 1
			# 	elif(item.status == 'Under Process'):
			# 		status_under_process += 1
			# 	elif(item.status == 'Form Submitted'):
			# 		status_form_submitted += 1
			# 	elif(item.status == 'Rejected'):
			# 		status_rejected += 1
			# 	elif(item.status == 'Completed'):
			# 		status_completed += 1
		# print("item status counts", status_open, status_under_process ,status_form_submitted , status_rejected , status_completed)
		# upper_value = (status_completed + status_rejected)
		# lower_value = (status_completed + status_rejected + status_open + status_under_process + status_form_submitted)
		# number_of_overall_status = str(upper_value) +'/'+ str(lower_value)
		# self.numeric_overall_status = number_of_overall_status
		# no_of_overall_status = number_of_overall_status
		# print("OVER ALL STATUS", number_of_overall_status , no_of_overall_status)

		if(self.head_of_family == 1):
			family_doc_name = frappe.get_list("Family",
        	filters={'head_of_family': self.name},
        	fields=["name"])
			if(family_doc_name):
				family_doc = frappe.get_doc("Family", family_doc_name[0].name)
				family_doc.name_of_parents = self.name_of_the_beneficiary
				family_doc.contact_number = self.contact_number
				family_doc.save()
			else:
				family_doc = frappe.new_doc("Family")
				family_doc.head_of_family = self.name
				family_doc.name_of_parents = self.name_of_the_beneficiary
				family_doc.contact_number = self.contact_number
				family_doc.insert()
				# update current beneficery to family
				self.family = family_doc.name
				# beneficiary.save()	
				frappe.msgprint("New Beneficary Update As a Head of Family")
		else:
			print("THis is beneficary is not a parent ")
