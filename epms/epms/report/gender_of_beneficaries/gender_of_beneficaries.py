# Copyright (c) 2023, Management System for Agrasarteach@suvaidyam.com and contributors
# For license information, please see license.txt

import frappe


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

	gender = frappe.get_all("Beneficiary",
	filters=new_filters,
	fields=["gender as gender",'count(name) as count'], 
	group_by='gender')
	print("gender", gender)

	# data = [{"gender":"Male" , "count":"0"},
	# 	 {"gender":"Female", "count":"0"}]
	data = gender
	chart = get_chart(data)
	return columns, data , None , chart , None

def get_chart(data):
	return{
		"data":{
			"labels":["Female","Male"],
			"datasets":[{"name":"Gender Composition", "values":{d["count"] for d in data}}]
		},
	"type":"pie"
	}