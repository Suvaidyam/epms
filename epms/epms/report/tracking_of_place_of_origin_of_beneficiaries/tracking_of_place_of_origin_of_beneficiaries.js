// Copyright (c) 2023, Management System for Agrasarteach@suvaidyam.com and contributors
// For license information, please see license.txt

frappe.query_reports["Tracking of place of origin of beneficiaries"] = {
	'filters': [
		{
			"fieldname":"from_date",
			"fieldtype":"Date",
			"label":"From Date",
		},
		{
			"fieldname":"to_date",
			"fieldtype":"Date",
			"label":"To Date"
		},
		{
			"fieldname":"state",
			"fieldtype":"Link",
			"label":"State",
			"options":"State"
		}
	]
	
};
// var newFilter = {
//     "fieldname": "city",
//     "fieldtype": "Data",  // You can adjust the field type as needed
//     "label": "City"
// };

// filters.push(newFilter);