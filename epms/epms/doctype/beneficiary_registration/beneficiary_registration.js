// Copyright (c) 2023, Management System for Agrasarteach@suvaidyam.com and contributors
// For license information, please see license.txt

frappe.ui.form.on("Beneficiary Registration", {
  refresh(frm) {
    var id_section = frm.get_field('id_section');
    if (frm.doc.do_you_have_id_document === 'Yes') {
        id_section.df.hidden = 0;
        id_section.refresh();
    } else {
        id_section.df.hidden = 1;
        id_section.refresh();
    }

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
          frm.set_value('date_of_visit', frappe.datetime.get_today());
          // frm.set_value('contact_number', '+91')
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
  },
  do_you_have_id_document: function(frm){
      var id_section = frm.get_field('id_section');
        if (frm.doc.do_you_have_id_document === 'Yes') {
            id_section.df.hidden = 0;
            id_section.refresh();
        } else {
            id_section.df.hidden = 1;
            id_section.refresh();
  }
  }

    
});
