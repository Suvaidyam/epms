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

	sql_query = """
	SELECT 
    s.support as support_name,
    s.support_type as support_category,
    (select count(parent) from `tabSupport Child` _sc where _sc.specific_support_type = s.support ) as enquiry_count,
    (select count(parent) from `tabSupport Child` _sc where _sc.specific_support_type = s.support and status = 'Completed' ) as achieved_count,
    (select count(parent) from `tabSupport Child` _sc where _sc.specific_support_type = s.support and status = 'Rejected' ) as rejected_count,
    (select count(parent) from `tabSupport Child` _sc where _sc.specific_support_type = s.support and status in ('','Open','Under Process','Form Submitted') ) as pending_count
	FROM
    `tabSupport` s
	"""

	result = frappe.db.sql(sql_query, as_dict=True)
	print(result)
	data = result
	return columns, data
