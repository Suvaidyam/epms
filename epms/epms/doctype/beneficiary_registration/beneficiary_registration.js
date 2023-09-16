// Copyright (c) 2023, Management System for Agrasarteach@suvaidyam.com and contributors
// For license information, please see license.txt

frappe.ui.form.on("Beneficiary Registration", {
	refresh(frm) {
        frm.fields_dict["district"].get_query = function (doc) {
            return {
              filters: {
                State: "please select state first",
              },
            };
          }
          frm.fields_dict["block"].get_query = function (doc) {
            return {
              filters: {
                District: "please select district first",
              },
            };
          }
	},
  state: function(frm){
    frm.fields_dict["district"].get_query = function (doc) {
      return {
        filters: {
          State: frm.doc.state,
        },
      };
    }
  },
  district: function(frm){
    frm.fields_dict["block"].get_query = function (doc) {
      return {
        filters: {
          District: frm.doc.district,
        },
      };
    }
  }

    
});
