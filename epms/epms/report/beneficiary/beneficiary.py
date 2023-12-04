# Copyright (c) 2023, Management System for Agrasarteach@suvaidyam.com and contributors
# For license information, please see license.txt

import frappe
from epms.utils.filter import Filter

def execute(filters=None):
	# frappe.errprint(filters)
	# columns = [
	# 	{
	# 	"fieldname":"beneficary",
	# 	"label":"Bank account status of the beneficiaries",
	# 	"fieldtype":"Data",
	# 	"width":400
	# 	},
	# 	{
	# 	"fieldname":"count",
	# 	"label":"Count",
	# 	"fieldtype":"int",
	# 	"width":100
	# 	}
	# ]
	meta = frappe.get_meta('Beneficiary')
	filtered_fields = [{"label": field.label, "fieldtype": field.fieldtype ,"fieldname": field.fieldname, "options":field.options} for field in meta.fields if field.fieldtype]
	new_filters = Filter.set_report_filters(filters, 'registration_date')
	# bank_account_data = frappe.get_all("Beneficiary",filters=filters, fields=["do_you_have_bank_account as have_account",'count(name) as count'], group_by='do_you_have_bank_account')
	bank_account_data = frappe.get_all("Beneficiary",
	filters=new_filters,
	fields=["*" , "occupation.occupation as 'occupation'", "csc.csc_name as 'csc'","state_of_origin.state_name as 'state_of_origin'" , "district_of_origin.district_name as 'district_of_origin'",
		 "block_of_origin.block_name as 'block_of_origin'" , "current_location.name_of_location as 'current_location'" , "family.name_of_parents as 'family'"])


	print("///////////////////////////////////////////////////", bank_account_data)
	data = bank_account_data
	# data = []
	# chart = get_chart(columns , [yes_count, no_count])


	return filtered_fields, data ,None