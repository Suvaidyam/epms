# Copyright (c) 2023, Management System for Agrasarteach@suvaidyam.com and contributors
# For license information, please see license.txt

import frappe
from epms.utils.filter import Filter


def execute(filters=None):
	columns = [
		{
			"fieldname":"support_category",
			"label":"Support category",
			"fieldtype":"Link",
			"options":"Support Type",
			"width":200
		},
		{
			"fieldname":"support_name",
			"label":"Support Name",
			"fieldtype":"Link",
			"options":"Support",
			"width":300
		},
		{
			"fieldname":"enquiry_count",
			"label":"No. of enquiries received",
			"fieldtype":"int",
			"width":200
		},
		{
			"fieldname":"achieved_count",
			"label":"Achieved",
			"fieldtype":"int",
			"width":100
		},
		{
			"fieldname":"rejected_count",
			"label":"Rejected",
			"fieldtype":"int",
			"width":100
		},
		{
			"fieldname":"pending_count",
			"label":"Pending",
			"fieldtype":"int",
			"width":100
		}
	]
	ben_filters = frappe._dict()
	other_filters = frappe._dict()
	for key in filters:
		if key in ['from_date','to_date','registration_date', 'csc']:
			ben_filters[key] = filters[key]
		else:
			other_filters[key] = filters[key]
	# print("ben_filters",ben_filters, "other_filters",other_filters, type(ben_filters), type(filters))

	ben_condition_str = Filter.set_report_filters(ben_filters, 'registration_date', True, '')
	support_condition_str = Filter.set_report_filters(other_filters, '', True, 's')

	if ben_condition_str:
		ben_condition_str = f"AND {ben_condition_str}"
	if support_condition_str:
		support_condition_str = f" WHERE {support_condition_str}"
	sql_query = f"""
		with beneficiary_report as (
			select
			_sc.specific_support_type,
			_sc.status,
			count(distinct tabBeneficiary.name) as ben_count
			from
				`tabSupport Child` _sc
			inner join tabBeneficiary on (tabBeneficiary.name = _sc.parent and _sc.parenttype = 'Beneficiary' {ben_condition_str})
			group by _sc.specific_support_type,_sc.status
		)

		select
			s.support_type as support_category,
			s.support as support_name,
			(select SUM(ben_count) as count from beneficiary_report _sc where _sc.specific_support_type = s.support ) as enquiry_count,
			(select sum(ben_count) as count from beneficiary_report _sc where _sc.specific_support_type = s.support and status = 'Completed') as achieved_count,
			(select sum(ben_count) as count from beneficiary_report _sc where _sc.specific_support_type = s.support and status = 'Rejected' ) as rejected_count,
			(select sum(ben_count) as count from beneficiary_report _sc where _sc.specific_support_type = s.support and status in ('','Open','Under Process','Form Submitted') ) as pending_count
		from
			`tabSupport` s
		{support_condition_str}
		order by support_category,support_name
	"""

	result = frappe.db.sql(sql_query, as_dict=True)
	# print(sql_query)
	data = result
	return columns, data
