# Copyright (c) 2023, Management System for Agrasarteach@suvaidyam.com and contributors
# For license information, please see license.txt

import frappe
from epms.utils.cache import Cache

def execute(filters=None):
	frappe.errprint(filters)
	columns = [
		{
		"fieldname":"gender",
		"label":"Gender composition",
		"fieldtype":"Data",
		"width":300
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

	gender = frappe.get_all("Beneficiary",
	filters=new_filters,
	fields=["gender as gender",'count(name) as count'],
	group_by='gender')

	# data = [{"gender":"Male" , "count":"0"},
	# 	 {"gender":"Female", "count":"0"}]
	data = gender
	chart = get_chart(data)
	return columns, data , None , chart , None

def get_chart(data):
	return{
		"data":{
			"labels":["Female","Male"],
			"datasets":[{"name":"Gender Composition", "values":(d["count"] for d in data)}]
		},
		"type":"pie"
	}