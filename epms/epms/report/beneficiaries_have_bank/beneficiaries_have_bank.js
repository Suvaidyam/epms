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
if (true) {
	filters.push({
		"fieldname": "csc",
		"fieldtype": "Link",
		"label": "CSC",
		"options": "CSC"
	})
}
// console.log(frappe.user_roles.includes(!"MIS executive"))
frappe.query_reports["Beneficiaries have Bank"] = {
	"filters": filters
};
