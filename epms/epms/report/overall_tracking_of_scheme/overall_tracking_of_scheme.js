// Copyright (c) 2023, Management System for Agrasarteach@suvaidyam.com and contributors
// For license information, please see license.txt

let filters = [
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
		"fieldname": "Support_category",
		"fieldtype": "Link",
		"options":"Support Type",
		"label": "Support category"
	}
];
if (true) {
	filters.push({
		"fieldname": "csc",
		"fieldtype": "Link",
		"label": "CSC",
		"options": "CSC"
	})
}
frappe.query_reports["Overall tracking of scheme"] = {
	"filters": filters
};
