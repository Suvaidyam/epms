# Copyright (c) 2023, Management System for Agrasarteach@suvaidyam.com and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	frappe.errprint(filters)
	columns = [
		{
		"fieldname":"education",
		"label":"Education",
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


	new_filters =None
	education = frappe.get_all("Beneficiary",
	filters=new_filters,
	fields=["education as education",'count(name) as count'], 
	group_by='education')
	print("education", education)
	data = education
	return columns, data
