// Copyright (c) 2023, Management System for Agrasarteach@suvaidyam.com and contributors
// For license information, please see license.txt

frappe.query_reports["Beneficiaries have Bank"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"fieldtype":"Date",
			"label":"From Date",
			"options": frappe.datetime.get_today()
		},
		{
			"fieldname":"to_date",
			"fieldtype":"Date",
			"label":"To Date"
		}
	]
};
