# Copyright (c) 2023, Management System for Agrasarteach@suvaidyam.com and contributors
# For license information, please see license.txt

import frappe
from epms.utils.filter import Filter

def execute(filters=None):
	# frappe.errprint(filters)
	columns = [
		{
		"fieldname":"beneficary",
		"label":"Bank account status of the beneficiaries",
		"fieldtype":"Data",
		"width":400
		},
		{
		"fieldname":"count",
		"label":"Count",
		"fieldtype":"int",
		"width":100
		}
	]
	new_filters = Filter.set_report_filters(filters, 'registration_date')
	# bank_account_data = frappe.get_all("Beneficiary",filters=filters, fields=["do_you_have_bank_account as have_account",'count(name) as count'], group_by='do_you_have_bank_account')
	bank_account_data = frappe.get_all("Beneficiary",
	filters=new_filters,
	fields=["do_you_have_bank_account as have_account",'count(name) as count'],
	group_by='do_you_have_bank_account')

	yes_count, no_count = 0, 0
	for acc in bank_account_data:
		if acc.have_account == 'Yes':
			yes_count += acc.count
		else:
			no_count += acc.count

	data = [{"beneficary":"Beneficiaries with one or more bank accounts" , "count":yes_count},
		 {"beneficary":"Beneficiaries with no bank account", "count":no_count}]
	# data = []
	# chart = get_chart(columns , [yes_count, no_count])


	return columns, data ,None

# def get_chart(columns,data):
# 	return{
# 		"data":{
# 			"labels":["Beneficiaries have bank account","Beneficiaries have not bank account"],
# 			"datasets":[{"name":"Beneficiaries have bank Account", "values":data}]
# 		},
# 		"type":"pie"
# 	}
