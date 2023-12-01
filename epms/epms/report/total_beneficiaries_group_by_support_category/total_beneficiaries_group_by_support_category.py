# Copyright (c) 2023, Management System for Agrasarteach@suvaidyam.com and contributors
# For license information, please see license.txt

import frappe
from epms.utils.filter import Filter

def execute(filters=None):
	frappe.errprint(filters)
	columns = [
		{
		"fieldname":"support_type",
		"label":"Support category",
		"fieldtype":"Link",
		"options":"Support Type",
		"width":400
		},
		{
		"fieldname":"count",
		"label":"Count",
		"fieldtype":"int",
		"width":200
		}
	]
	condition_str = Filter.set_report_filters(filters, 'date_of_application', True)
	if condition_str:
		condition_str = f"{condition_str}" + f"support_type IN ('Govt. Schemes', 'Documentation', 'Bank A/C')"
	else:
		condition_str = "1=1"

	sql_query = f"""
SELECT 
  sc.support_type,
  COUNT(DISTINCT sc.parent) AS count,
  b.csc
FROM 
  `tabSupport Child` sc
JOIN
  `tabBeneficiary` b ON sc.parent = b.name
WHERE 
  sc.support_type IN ('Govt. Schemes', 'Documentation', 'Bank A/C') 
  AND sc.date_of_application = '2023-11-30' and b.csc = 'CSC-S10-003'
GROUP BY
  sc.support_type;
	"""
	print("sql_query",sql_query)
	data = frappe.db.sql(sql_query, as_dict=True)
	return columns, data
