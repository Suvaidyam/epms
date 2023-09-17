# Copyright (c) 2023, Management System for Agrasarteach@suvaidyam.com and contributors
# For license information, please see license.txt

import frappe
import json
from frappe.model.document import Document

class Beneficiary(Document):

	def after_insert(self):
    # Your custom code here
			print("/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////")	
			print("Self data",self)
			print("document",Document)
			frappe.msgprint("after insert call")

