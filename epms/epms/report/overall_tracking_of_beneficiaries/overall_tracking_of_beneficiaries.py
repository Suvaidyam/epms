# Copyright (c) 2023, Management System for Agrasarteach@suvaidyam.com and contributors
# For license information, please see license.txt

import frappe
from epms.utils.cache import Cache


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

	ben = frappe.get_all("Beneficiary",
	filters=new_filters,
	fields=["head_of_family as beneficary",'count(name) as count'],
	group_by='head_of_family')

	global no_family , no_ben
	no_family, no_ben = 0 ,0
	for entry in ben:
		# print(entry)
		if entry['beneficary'] == 'No':
			entry['beneficary'] = 'Family'
			no_family = entry['count']
		else:
			entry['beneficary'] = 'Beneficiary'
			no_ben = entry['count']
			# entry['count'] = (entry['count'] + no_family)
	for data in ben:
		if data['beneficary'] == 'Yes':
			data['count'] = no_family + no_ben
			# print("///////", data['count'])
	print(ben)
	# print(no_family + no_ben)
	data = ben
	return columns, data
