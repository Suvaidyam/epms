# Copyright (c) 2023, Management System for Agrasarteach@suvaidyam.com and contributors
# For license information, please see license.txt
import frappe
from epms.utils.filter import Filter


def execute(filters=None):
    columns = [
        {
            "fieldname": "support_type",
            "label": "Support category",
            "fieldtype": "Link",
            "options": "Support Type",
            "width": 200
        },
        {
            "fieldname": "count",
            "label": "Applied",
            "fieldtype": "Int",
            "width": 200
        },
        {
            "fieldname": "comp_count",
            "label": "Application Completed",
            "fieldtype": "Int",
            "width": 100
        }
    ]

    support_filters = frappe._dict()
    ben_filters = frappe._dict()

    for key in filters:
        if key in ['registration_date', 'csc']:
            ben_filters[key] = filters[key]
        elif key in ['from_date', 'to_date']:
            support_filters[key] = filters[key]

    comp_condition_str = Filter.set_report_filters(
        support_filters, 'date_of_completion', True, '', False)
    ben_condition_str = Filter.set_report_filters(
        ben_filters, 'registration_date', True, 'tabBeneficiary')

    if ben_condition_str:
        ben_condition_str = f"AND parent in (select name from `tabBeneficiary` where {ben_condition_str})"
    if comp_condition_str:
        comp_condition_str = f"AND {comp_condition_str}"

    sql_query = f"""

		SELECT
			support_type,
			COUNT(DISTINCT parent) AS count,
			SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) AS comp_count
		FROM (
			SELECT DISTINCT parent, support_type, status
			FROM `tabSupport Child`
			WHERE 1=1 {ben_condition_str} {comp_condition_str}
		) AS distinct_parents
		GROUP BY
			support_type;
    """
    print(sql_query)
    result = frappe.db.sql(sql_query, as_dict=True)
    data = result
    return columns, data
