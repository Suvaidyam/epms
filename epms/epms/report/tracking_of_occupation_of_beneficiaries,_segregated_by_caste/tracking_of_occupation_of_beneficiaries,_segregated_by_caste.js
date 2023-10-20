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
		"fieldname":"caste",
		"label":"Caste",
		"fieldtype":"Link",
		"options":"Caste master"
	},
	{
		"fieldname":"occupations",
		"label":"occupations",
		"fieldtype":"Link",
		"options":"Current Occupation",
		"width":300
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
frappe.query_reports["Tracking of Occupation of beneficiaries, segregated by Caste"] = {
	"filters": filters
};
