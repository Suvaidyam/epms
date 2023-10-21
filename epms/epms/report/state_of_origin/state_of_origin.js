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
frappe.query_reports["State Of Origin"] = {
	"filters": filters
};
