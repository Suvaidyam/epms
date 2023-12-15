# Copyright (c) 2023, Management System for Agrasarteach@suvaidyam.com and contributors
# For license information, please see license.txt

import frappe
from epms.utils.filter import Filter


def execute(filters=None):
    ben_meta = frappe.get_meta('Beneficiary')
    support_meta = frappe.get_meta('Support Child')
    followup_meta = frappe.get_meta('Follow Up Child')
    allowed_types = ['Data', 'Int', 'Select', 'Link', 'Check']

    filtered_fields = [
        {"label": field.label, "fieldtype": field.fieldtype,
         "fieldname": field.fieldname, "options": field.options}
        for field in ben_meta.fields if field.fieldtype in allowed_types
    ]

    filtered_fields.extend([
        {"label": field.label, "fieldtype": field.fieldtype,
         "fieldname": field.fieldname, "options": field.options}
        for field in support_meta.fields if field.fieldtype in allowed_types
    ])

    filtered_fields.extend([
        {"label": field.label, "fieldtype": field.fieldtype,
         "fieldname": field.fieldname, "options": field.options}
        for field in followup_meta.fields if field.fieldtype in allowed_types
    ])

    # Construct a list of column names for the SQL SELECT statement
    columns = [
        f"`{field['fieldname']}`" for field in filtered_fields]

    # Add additional columns to the list if needed
    columns.append("`state`.`state_name`")

    # Construct the SQL query
    sql_query = f"""
        SELECT
            {', '.join(columns)},
			state.state_name as state_of_origin
        FROM
            `tabBeneficiary` ben
        LEFT JOIN `tabState` state ON state.name = ben.state_of_origin
        LEFT JOIN `tabSupport Child` support_child ON (support_child.parent = ben.name AND support_child.parenttype = 'Beneficiary')
        LEFT JOIN `tabFollow Up Child` follow_up_child ON (follow_up_child.parent = ben.name AND follow_up_child.parenttype = 'Beneficiary')
    """

    # Execute the SQL query
    data = frappe.db.sql(sql_query)

    return filtered_fields, data, None
