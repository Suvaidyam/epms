// Copyright (c) 2023, Management System for Agrasarteach@suvaidyam.com and contributors
// For license information, please see license.txt

frappe.ui.form.on("Beneficiary", {
  refresh(frm) {
    console.log(frm.sidebar)
  //  ID PROOF SECTION LOGIC FOR SHOW AND HIDE SECTION
    var id_section = frm.get_field('id_section');
    if (frm.doc.do_you_have_id_document === 'Yes') {
        id_section.df.hidden = 0;
        id_section.refresh();
    } else {
        id_section.df.hidden = 1;
        id_section.refresh();
    }
// CURRENT RESIDENT DEPENDENT DROPDOWNS LOGICS
        frm.fields_dict["current_district"].get_query = function (doc) {
            return {
              filters: {
                State: "please select Current state",
              },
            };
          }
        frm.fields_dict["current_block"].get_query = function (doc) {
            return {
              filters: {
                District: "please select Current district",
              },
            };
          }
//  ORIGIN RESIDENT DEPENDENT DROPDOWNS LOGICS
                frm.fields_dict["district_of_origin"].get_query = function (doc) {
            return {
              filters: {
                State: "please select state of origin",
              },
            };
          }
        frm.fields_dict["current_block"].get_query = function (doc) {
            return {
              filters: {
                District: "please select district of origin",
              },
            };
          }

// DEFULTS DATE SET 
          frm.set_value('date_of_visit', frappe.datetime.get_today());
          frm.set_df_property('date_of_visit', 'read_only', 1);

	},

//  field wise dependent dropdowns
  state_of_origin: function(frm){
    frm.fields_dict["district_of_origin"].get_query = function (doc) {
      return {
        filters: {
          State: frm.doc.state_of_origin,
        },
      };
    }
  },
  district_of_origin: function(frm){
    frm.fields_dict["block_of_origin"].get_query = function (doc) {
      return {
        filters: {
          District: frm.doc.district_of_origin,
        },
      };
    }
  },
  current_state: function(frm){
    frm.fields_dict["current_district"].get_query = function (doc) {
      return {
        filters: {
          State: frm.doc.current_state,
        },
      };
    }
  },
  current_district: function(frm){
    frm.fields_dict["current_block"].get_query = function (doc) {
      return {
        filters: {
          District: frm.doc.current_district,
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
  },
  are_you_parents:function(frm){
    var parentField = frm.fields_dict['family'];
    if(frm.doc.are_you_parents){
      parentField.df.hidden = 1;
      parentField.refresh();
    }else{
      parentField.df.hidden = 0;
      parentField.refresh();
    }
  },
  date_of_birth:function(frm){
    let dob = frm.doc.date_of_birth
    let year = frappe.datetime.get_today()
    let age = year.split('-')[0] - dob.split('-')[0]
    frm.set_value('age', age)
    frm.set_df_property('age', 'read_only', 1);
  }
});
