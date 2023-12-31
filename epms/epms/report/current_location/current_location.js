// Copyright (c) 2023, Management System for Agrasarteach@suvaidyam.com and contributors
// For license information, please see license.txt
if (!frappe.user_roles.includes("MIS executive") || frappe.user_roles.includes("Administrator")) {
	setTimeout(()=>{[...document.querySelectorAll("[data-label='Edit']"),...document.querySelectorAll("[data-action='action-edit']")].forEach(e=> e.remove())},500)
}
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
	}
	
];
if (!frappe.user_roles.includes("MIS executive") || frappe.user_roles.includes("Administrator")) {
	filters.push({
		"fieldname": "csc",
		"fieldtype": "Link",
		"label": "Centre",
		"options": "Centre"
	})
}
frappe.query_reports["Current Location"] = {
	filters: filters
};
