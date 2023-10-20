# Copyright (c) 2023, Management System for Agrasarteach@suvaidyam.com and contributors
# For license information, please see license.txt

import frappe
from epms.utils.filter import Filter


def execute(filters=None):

	columns = [
		{
			"fieldname":"beneficary",
			"label":"Over tracking of beneficaries",
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

	results = frappe.get_all("Beneficiary",
	filters=new_filters,
	fields=["head_of_family as beneficary",'count(name) as count'],
	group_by='head_of_family')

	no_family, no_ben = 0 ,0
	for entry in results:
		if entry['beneficary'] == 'No':
			no_family = entry['count']
		else:
			no_ben = entry['count']
	data = [
    	{'beneficary':'No. of beneficiaries', 'count':(no_ben+no_family)},
     	{'beneficary':'No. of families', 'count':(no_family)}
    ]
	return columns, data
