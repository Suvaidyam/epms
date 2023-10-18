# Copyright (c) 2023, Management System for Agrasarteach@suvaidyam.com and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	frappe.errprint(filters)
	columns = [
		{
		"fieldname":"beneficary",
		"label":"beneficary",
		"fieldtype":"Data",
		"width":400
		},
		{
		"fieldname":"count",
		"label":"Count",
		"fieldtype":"int",
		"width":400
		}
	]

	bank_account_data = frappe.get_all("Beneficiary",filters=filters, fields=["do_you_have_bank_account as have_account",'count(name) as count'], group_by='do_you_have_bank_account')

	have_bank_account = 0
	have_not_bank_account = 0
	
	# for bank in bank_account_data:
	# 	print(bank)
	# 	if bank.bank_account_data == 'Yes':
	# 		have_bank_account = have_bank_account + 1
	# 	else:
	# 		have_not_bank_account = have_not_bank_account + 1

	# sql_query = """
	# SELECT do_you_have_bank_account
	# FROM `tabBeneficiary`
	# """
	# frappe.db.sql(sql_query)
	

	data = [{"beneficary":"No. of beneficary have bank account" , "count":have_bank_account},
		 {"beneficary":"No. of beneficary have not bank account", "count":have_not_bank_account}]




	return columns, data
