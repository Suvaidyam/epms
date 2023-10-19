# Copyright (c) 2023, Management System for Agrasarteach@suvaidyam.com and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
	frappe.errprint(filters)
	columns = [
		{
		"fieldname":"location",
		"label":"Current location",
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
	location = frappe.get_all("Beneficiary",
	filters=new_filters,
	fields=["current_location as location",'count(name) as count'], 
	group_by='current_location')
	print("education", location)
	data = location
	return columns, data
