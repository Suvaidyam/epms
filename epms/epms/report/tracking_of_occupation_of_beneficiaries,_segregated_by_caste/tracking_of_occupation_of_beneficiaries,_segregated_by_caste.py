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

	sql_query = """
	SELECT _o.occupation as occupations, caste,  COUNT(_b.name) AS count
	FROM `tabCurrent Occupation` _o
	LEFT JOIN `tabBeneficiary` _b ON _b.occupation = _o.name
	GROUP BY _o.occupation;
	"""

	result = frappe.db.sql(sql_query, as_dict=True)

	print(result)


	data = result
	return columns, data
