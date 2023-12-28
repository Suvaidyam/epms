# Copyright (c) 2023, Management System for Agrasarteach@suvaidyam.com and contributors
# For license information, please see license.txt

import frappe
from epms.utils.filter import Filter

def execute(filters=None):
	columns = [
		{
		"fieldname":"saving_status",
		"label":"Saving Status",
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
	condition_str = Filter.set_report_filters(filters, 'registration_date', True)
	if condition_str:
		condition_str = f"{condition_str}"
	else:
		condition_str = "1=1"

	sql_query = f"""
	SELECT saving_status, COUNT(name) AS count
	FROM tabBeneficiary
	WHERE saving_status IS NOT NULL AND saving_status <> '' AND {condition_str}
	GROUP BY saving_status;
	"""
	data = frappe.db.sql(sql_query, as_dict=True)
	return columns, data
