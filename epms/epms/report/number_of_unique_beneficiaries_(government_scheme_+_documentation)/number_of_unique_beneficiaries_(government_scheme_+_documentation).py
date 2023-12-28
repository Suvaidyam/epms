# Copyright (c) 2023, Management System for Agrasarteach@suvaidyam.com and contributors
# For license information, please see license.txt

# Copyright (c) 2023, Management System for Agrasarteach@suvaidyam.com and contributors
# For license information, please see license.txt

import frappe
from epms.utils.filter import Filter


def execute(filters=None):
    columns = [

        {
            "fieldname": "comp_count",
            "label": "Unique beneficiary count",
            "fieldtype": "Int",
            "width": 300
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
 	SELECT count(DISTINCT parent) as comp_count
    FROM `tabSupport Child`
    WHERE support_type IN ('Documentation', 'Government Scheme') AND status = 'Completed' AND 1=1 {ben_condition_str} {comp_condition_str}
    """
    result = frappe.db.sql(sql_query, as_dict=True)
    return columns, result

