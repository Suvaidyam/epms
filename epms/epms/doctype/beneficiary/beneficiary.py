# Copyright (c) 2023, Management System for Agrasarteach@suvaidyam.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from epms.utils.cache import Cache
from epms.services.primary_member import Primary_member

class Beneficiary(Document):
	def validate(self):
		if not self.csc:
			self.csc = Cache.get_csc()
	def after_insert(self):
		# if other select then auto add in list next time
		if(self.new_occupation):
			new_occupation_doc = frappe.new_doc("Current Occupation")
			new_occupation_doc.occupation = self.new_occupation
			new_occupation_doc.save()
		# if(self.other_bank_account):
		# 	new_bank_doc = frappe.new_doc("Bank")
		# 	new_bank_doc.bank_name = self.other_bank_account
		# 	new_bank_doc.save()
		if(self.other_current_location):
			new_location_doc = frappe.new_doc("Current location")
			if(self.csc):
				new_location_doc.centre = self.csc
			else:
				new_location_doc.centre = Cache.get_csc()
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
		# beneficiary.csc = Cache.get_csc()
		if(self.head_of_family == "No"):
			# To Create primary member
			family_doc = Primary_member.create_family(beneficiary)
			# update current beneficery
			frappe.db.set_value('Beneficiary', self.name, 'family', family_doc.name, update_modified=False)
		else:
			# beneficiary.save()
			print("CREATING CHILD BENEFICARY")

	def on_update(self):
		if(self.head_of_family == "No"):
			# update primary members
			family_doc = Primary_member.update_family(self)
			if not self.family:
				frappe.db.set_value('Beneficiary', self.name, 'family', family_doc.name, update_modified=False)
		else:
			Primary_member.delete_family(self)
