# Copyright (c) 2023, Management System for Agrasarteach@suvaidyam.com and contributors
# For license information, please see license.txt

import frappe
from epms.utils.filter import Filter

def execute(filters=None):
	# frappe.errprint(filters)
	columns = [
		{
			"fieldname":"education",
			"label":"Education of beneficiary",
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
	new_filters = Filter.set_report_filters(filters, 'registration_date')


	data = frappe.get_all("Beneficiary",
	filters=new_filters,
	fields=["education as education",'count(name) as count'],
	group_by='education')

	for result in data:
		if result.education is None:
			result.education = 'None'
	return columns, data
