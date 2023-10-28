// Copyright (c) 2023, Management System for Agrasarteach@suvaidyam.com and contributors
// For license information, please see license.txt

frappe.ui.form.on("Centre", {
	refresh(frm) {
        frm.set_query("state", () => {
            return { page_length: 1000 };
          });
          frm.set_query("district", () => {
            return { page_length: 1000 };
          });
        frm.fields_dict["district"].get_query = function (doc) {
            return {
              filters: {
                state: "please select state",
              },
            };
          }
	},
    state:function(frm){
        frm.fields_dict["district"].get_query = function (doc) {
            return {
              filters: {
                state: frm.doc.state,
              },
            };
          }
    }
    
});
