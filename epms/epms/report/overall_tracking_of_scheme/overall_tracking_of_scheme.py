# Copyright (c) 2023, Management System for Agrasarteach@suvaidyam.com and contributors
# For license information, please see license.txt

import frappe
from epms.utils.filter import Filter


def execute(filters=None):
    columns = [
        {
            "fieldname": "support_category",
            "label": "Support category",
            "fieldtype": "Link",
            "options": "Support Type",
            "width": 200
        },
        {
            "fieldname": "support_name",
            "label": "Support Name",
            "fieldtype": "Link",
            "options": "Support",
            "width": 300
        },
        {
            "fieldname": "enquiry_count",
            "label": "No. of enquiries received",
            "fieldtype": "int",
            "width": 200
        },
        {
            "fieldname": "achieved_count",
            "label": "Achieved",
            "fieldtype": "int",
            "width": 100
        },
        {
            "fieldname": "rejected_count",
            "label": "Rejected",
            "fieldtype": "int",
            "width": 100
        },
        {
            "fieldname": "pending_count",
            "label": "Pending",
            "fieldtype": "int",
            "width": 100
        }
    ]
    support_filters = frappe._dict()
    ben_filters = frappe._dict()
    other_filters = frappe._dict()

    for key in filters:
        if key in ['registration_date', 'csc']:
            ben_filters[key] = filters[key]
        elif key in ['from_date', 'to_date']:
            support_filters[key] = filters[key]
        else:
            other_filters[key] = filters[key]
    # print("ben_filters",ben_filters, "other_filters",other_filters, type(ben_filters), type(filters))

    enquiry_condition_str = Filter.set_report_filters(
        support_filters, 'creation', True, '_sc')
    achieved_condition_str = Filter.set_report_filters(
        support_filters, 'date_of_completion', True, '_sc')
    rejected_condition_str = Filter.set_report_filters(
        support_filters, 'date_of_rejection', True, '_sc')
    ben_condition_str = Filter.set_report_filters(
        ben_filters, 'registration_date', True, 'tabBeneficiary')
    support_master_condition_str = Filter.set_report_filters(
        other_filters, '', True, 's')

    if ben_condition_str:
        ben_condition_str = f"AND {ben_condition_str}"

    # support filter

    if enquiry_condition_str:
        enquiry_condition_str = f"AND {enquiry_condition_str}"

    if achieved_condition_str:
        achieved_condition_str = f"AND {achieved_condition_str}"
    if rejected_condition_str:
        rejected_condition_str = f"AND {rejected_condition_str}"

    if support_master_condition_str:
        support_master_condition_str = f" WHERE {support_master_condition_str}"

    sql_query = f"""
		with beneficiary_report as (
			select
			_sc.name,
   			_sc.specific_support_type,
			_sc.status,
			from
				`tabSupport Child` _sc
			inner join tabBeneficiary on (tabBeneficiary.name = _sc.parent and _sc.parenttype = 'Beneficiary' {ben_condition_str})
		)

		select
			s.support_type as support_category,
			s.support as support_name,
			(select SUM(ben_count) as count from beneficiary_report _sc where _sc.specific_support_type = s.support {enquiry_condition_str}) as enquiry_count,
			(select sum(ben_count) as count from beneficiary_report _sc where _sc.specific_support_type = s.support and status = 'Completed' {achieved_condition_str}) as achieved_count,
			(select sum(ben_count) as count from beneficiary_report _sc where _sc.specific_support_type = s.support and status = 'Rejected' {rejected_condition_str}) as rejected_count,
			(select sum(ben_count) as count from beneficiary_report _sc where _sc.specific_support_type = s.support and status in ('','Open','Under Process','Form Submitted') {enquiry_condition_str} ) as pending_count
		from
			`tabSupport` s
		{support_master_condition_str}
		order by support_category,support_name
	"""

    result = frappe.db.sql(sql_query, as_dict=True)
    print(sql_query)
    data = result
    return columns, data
