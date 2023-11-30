// Copyright (c) 2023, Management System for Agrasarteach@suvaidyam.com and contributors
// For license information, please see license.txt

var filters = [
	{
		"fieldname": "date_of_application",
		"fieldtype": "Date",
		"label": "Date of application",
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
frappe.query_reports["Total beneficiaries whose application is completed group by support category"] = {
	"filters": [

	]
};
