// Copyright (c) 2023, Management System for Agrasarteach@suvaidyam.com and contributors
// For license information, please see license.txt


function get_support_list(frm ,support_type){
    frappe.call({
      method: 'frappe.desk.search.search_link',
      args: {
        doctype: 'Support',
        txt: '',
        filters: [
          ['Support', 'support_type', '=', support_type],
        ],
        page_length: 100,  // Adjust the number of results per page as needed
      },
      freeze:true,
      freeze_message: __("Wait ..."),
      callback: async function(response) {
        frm.fields_dict.camp_child_table.grid.update_docfield_property("support_name","options", response.results);
      }});
  };
// //////////////////////////////////////////////////////////////////////
function get_support_types(frm){
    frappe.call({
      method: 'frappe.desk.search.search_link',
      args: {
        doctype: 'Support Type',
        txt: '',
        page_length: 100,  // Adjust the number of results per page as needed
      },
      freeze:true,
      freeze_message: __("Wait ..."),
      callback: async function(response) {
        frm.fields_dict.camp_child_table.grid.update_docfield_property("support_category","options", response.results);
      }}); 
  };
  // ///////////////////////////////////////////////////////////////////////
    // ///////////////////////////////////////////////////////////////////////
      // ///////////////////////////////////////////////////////////////////////
frappe.ui.form.on("Camp Form", {
	refresh(frm) {
	},
    before_save: function(frm){
        let number_of_participants =0;
        for(item of frm.doc?.camp_child_table){
            number_of_participants += item.number_of_participants
            console.log(item.number_of_participants)
        }
        frm.doc.number_of_participants = number_of_participants
    }
});

frappe.ui.form.on('Camp Form Child', {
    camp_child_table_add(frm, cdt, cdn) {
      let row = frappe.get_doc(cdt, cdn);
      get_support_types(frm)
      console.log(row)
    },
    support_category: function (frm, cdt, cdn) {
        let row = frappe.get_doc(cdt, cdn);
        get_support_list(frm,row.support_category)
    
      }
  })
