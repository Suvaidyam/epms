# Copyright (c) 2023, Management System for Agrasarteach@suvaidyam.com and contributors
# For license information, please see license.txt

import frappe
from epms.utils.filter import Filter


def execute(filters=None):
	columns = [
		{
			"fieldname":"caste",
			"label":"Caste",
			"fieldtype":"Link",
			"options":"Caste master",
			"width":200
		},
		{
			"fieldname":"occupations",
			"label":"occupations",
			"fieldtype":"Link",
			"options":"Current Occupation",
			"width":300
		},
		{
			"fieldname":"count",
			"label":"Count",
			"fieldtype":"int",
			"width":200
		}
	]
	condition_str = Filter.set_report_filters(filters, 'registration_date', True)
	if condition_str:
		condition_str = f"{condition_str}"
	else:
		condition_str = "1=1"
	sql_query = f"""
	SELECT _o.occupation as occupations, caste,  COUNT(_b.name) AS count
	FROM `tabCurrent Occupation` _o
	LEFT JOIN `tabBeneficiary` _b ON _b.occupation = _o.name
	WHERE {condition_str}
	GROUP BY _o.occupation;
	"""
	print("sql_query",sql_query)

	result = frappe.db.sql(sql_query, as_dict=True)

	print(result)


	data = result
	return columns, data
