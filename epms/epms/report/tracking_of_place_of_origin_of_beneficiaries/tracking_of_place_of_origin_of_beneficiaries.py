# Copyright (c) 2023, Management System for Agrasarteach@suvaidyam.com and contributors
# For license information, please see license.txt

import frappe
from epms.utils.cache import Cache


def execute(filters=None):
	columns = [
		{
		"fieldname":"state",
		"label":"State",
		"fieldtype":"Data",
		"width":400
		},
			{
		"fieldname":"district",
		"label":"District",
		"fieldtype":"Data",
		"width":400
		},
		{
		"fieldname":"count",
		"label":"Count",
		"fieldtype":"int",
		"width":200
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

	# count of beneficary according to state and district of origins
	state = frappe.get_all("Beneficiary",
	filters=new_filters,
	fields=[" district_of_origin as district",'count(`tabBeneficiary`.name) as count'],
	group_by='district_of_origin'
	)
	# print(state)
	data = []
	return columns, data