// Copyright (c) 2023, Management System for Agrasarteach@suvaidyam.com and contributors
// For license information, please see license.txt

var filters = [
	{
		"fieldname": "from_date",
		"fieldtype": "Date",
		"label": "From Date",
	},
	{
		"fieldname": "to_date",
		"fieldtype": "Date",
		"label": "To Date"
	},
	{
		"fieldname": "support_type",
		"fieldtype": "Link",
		"options": "Support Type",
		"label": "Support category"
	}
];
if (!frappe.user_roles.includes("MIS executive")) {
	filters.push({
		"fieldname": "csc",
		"fieldtype": "Link",
		"label": "CSC",
		"options": "CSC"
	})
}
frappe.query_reports["Overall tracking of scheme"] = {
	filters: filters
};
