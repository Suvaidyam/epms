# Copyright (c) 2023, Management System for Agrasarteach@suvaidyam.com and contributors
# For license information, please see license.txt

import frappe
from epms.utils.filter import Filter


def execute(filters=None):
    columns = [
        {
            "fieldname": "Age_Category",
            "label": "Age Category",
            "fieldtype": "Data",
            "width": 200
        },
        {
            "fieldname": "Number_of_People",
            "label": "Number of Beneficiary",
            "fieldtype": "int",
            "width": 300
        }
    ]
    condition_str = Filter.set_report_filters(
        filters, 'registration_date', True)
    if condition_str:
        condition_str = f"WHERE {condition_str}"
    else:
        condition_str = ""
    sql_query = f"""
SELECT
        'Less than 5 years' AS Age_Category, COUNT(CASE WHEN age < 5 THEN 1 END) AS Number_of_People
    FROM
        `tabBeneficiary`
    {condition_str}

    UNION ALL

    SELECT
        '5 - 10 years' AS Age_Category, COUNT(CASE WHEN age BETWEEN 5 AND 10 THEN 1 END) AS Number_of_People
    FROM
        `tabBeneficiary`
    {condition_str}

    UNION ALL

    SELECT
        '11 - 17 years' AS Age_Category, COUNT(CASE WHEN age BETWEEN 11 AND 17 THEN 1 END) AS Number_of_People
    FROM
        `tabBeneficiary`
    {condition_str}

    UNION ALL

    SELECT
        '18 - 40 years' AS Age_Category, COUNT(CASE WHEN age BETWEEN 18 AND 40 THEN 1 END) AS Number_of_People
    FROM
        `tabBeneficiary`
    {condition_str}

    UNION ALL

    SELECT
        '41 - 60 years' AS Age_Category, COUNT(CASE WHEN age BETWEEN 41 AND 60 THEN 1 END) AS Number_of_People
    FROM
        `tabBeneficiary`
    {condition_str}

    UNION ALL

    SELECT
        '60 years above' AS Age_Category, COUNT(CASE WHEN age > 60 THEN 1 END) AS Number_of_People
    FROM
        `tabBeneficiary`
    {condition_str}
	"""
    data = frappe.db.sql(sql_query, as_dict=True)
    return columns, data
