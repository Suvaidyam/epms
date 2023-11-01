# Copyright (c) 2023, Management System for Agrasarteach@suvaidyam.com and contributors
# For license information, please see license.txt

import frappe
from epms.utils.filter import Filter


def execute(filters=None):
    columns = [
        {
            "fieldname": "caste",
            "label": "Caste",
            "fieldtype": "Link",
            "options": "Caste master",
            "width": 200
        },
        {
            "fieldname": "occupation",
            "label": "Occupation",
            "fieldtype": "Link",
            "options": "Current Occupation",
            "width": 300
        },
        {
            "fieldname": "count",
            "label": "Count",
            "fieldtype": "int",
            "width": 200
        }
    ]
    condition_str = Filter.set_report_filters(
        filters, 'registration_date', True)
    if condition_str:
        condition_str = f"WHERE {condition_str}"
    else:
        condition_str = ""
    sql_query = f"""
		select
			occupation,
			caste,
			count(name) as count
		from
			`tabBeneficiary`
		{condition_str}
		group by caste, occupation
		order by caste ASC,occupation ASC

	"""
    data = frappe.db.sql(sql_query, as_dict=True)
    return columns, data
