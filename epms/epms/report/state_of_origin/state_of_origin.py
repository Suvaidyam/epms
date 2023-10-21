# Copyright (c) 2023, Management System for Agrasarteach@suvaidyam.com and contributors
# For license information, please see license.txt

import frappe
from epms.utils.filter import Filter

def execute(filters=None):
	# frappe.errprint(filters)
	columns = [
		{
			"fieldname":"state",
			"label":"State",
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
	fields=["state_of_origin.state_name as state",'count(`tabBeneficiary`.name) as count'],
	group_by='state')

	return columns, data