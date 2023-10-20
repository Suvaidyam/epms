# Copyright (c) 2023, Management System for Agrasarteach@suvaidyam.com and contributors
# For license information, please see license.txt

import frappe
from epms.utils.cache import Cache

def execute(filters=None):
	# frappe.errprint(filters)
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
	new_filters = None
	if filters:
		if filters.from_date and filters.to_date:
			new_filters={ "registration_date": ["between", [filters.from_date, filters.to_date]]}
		elif filters.from_date:
			new_filters={ "registration_date": [">=", filters.from_date]}
		elif filters.to_date:
			new_filters={ "registration_date": ["<=", filters.to_date]}
	else:
		new_filters= {}

	csc =None
	user = frappe.session.user
	if "MIS executive" in frappe.get_roles(user) and ("Administrator" not in frappe.get_roles(user)):
		csc = Cache.get_csc()
		new_filters["csc"] = csc
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

	data = [{"beneficary":"No. of beneficary have bank account" , "count":yes_count},
		 {"beneficary":"No. of beneficary have not bank account", "count":no_count}]
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
