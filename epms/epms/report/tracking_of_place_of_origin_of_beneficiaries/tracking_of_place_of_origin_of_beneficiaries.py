# Copyright (c) 2023, Management System for Agrasarteach@suvaidyam.com and contributors
# For license information, please see license.txt

import frappe
from epms.utils.filter import Filter

def execute(filters=None):
	columns = [
		{
		"fieldname":"state",
		"label":"State",
		"fieldtype":"Data",
		"width":400
		},
			{
		"fieldname":"district",
		"label":"District",
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
	condition_str = Filter.set_report_filters(filters, 'registration_date', True)
	if condition_str:
		condition_str = f"{condition_str}"
	else:
		condition_str = "1=1"

	sql_query = f"""
	SELECT  s.state_name as state, d.district_name as district, COUNT(b.name) AS count
	FROM tabBeneficiary AS b
	JOIN tabState AS s JOIN tabDistrict AS d ON b.state_of_origin = s.name AND b.district_of_origin = d.name
	WHERE {condition_str}
 	GROUP BY state_of_origin, district_of_origin
	ORDER BY state_of_origin, district_of_origin;;
	"""

	result = frappe.db.sql(sql_query, as_dict=True)
	print(result)
	data = result
	return columns, data
