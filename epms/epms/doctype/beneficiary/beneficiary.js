// Copyright (c) 2023, Management System for Agrasarteach@suvaidyam.com and contributors
// For license information, please see license.txt
var global_data = []
frappe.ui.form.on("Beneficiary", {
  before_save:function(frm){
        // follow up status manage
    if(frm.selected_doc.followup_table){
      for(follow_up_items of frm.selected_doc.followup_table){
        let support_name = follow_up_items.support_name;
        for(support_items of frm.selected_doc.support_table){
          if(support_items.specific_support_type === support_name){
            if(follow_up_items.follow_up_status === "Not interested"){
              support_items.status = "Closed"
            }else if(follow_up_items.follow_up_status === "interested"){
                if(support_items.status === 'Closed'){
                  support_items.status = "Open"
                }
            }else{
              support_items.status = follow_up_items.follow_up_status
            }
          } 
        }
      }
    }

    console.log("before save " , frm.selected_doc.support_table)
    let open , under_process , form_submitted , rejected , completed , closed;
    open = under_process = form_submitted = rejected = completed = closed = 0;
    let total_no_of_support  = 0
    for(item of frm.selected_doc.support_table){
        global_data.push(item)
        ++total_no_of_support
        if(item.status === 'Open'){
          ++open
        }else if(item.status === 'Under Process'){
          ++under_process
        }else if(item.status == 'Form Submitted'){
          ++form_submitted
        }else if(item.status == 'Rejected'){
          ++rejected
        }else if(item.status == 'Completed'){
          ++completed
        }else{
          ++closed
        }
    }
    let numberic_overall_status = (completed + rejected) + '/' + (completed + rejected + form_submitted + under_process + open)
    // console.log(open , under_process,form_submitted , rejected , completed)
    frm.doc.numeric_overall_status = numberic_overall_status;
    // console.log(numberic_overall_status , total_no_of_support)
    if(total_no_of_support === open){
      frm.doc.overall_status = 'Open'
    }else if(total_no_of_support === completed){
      frm.doc.overall_status = 'Completed'
    }else{
      if(total_no_of_support === open + under_process + form_submitted){
        frm.doc.overall_status = 'Open'
      }else if(total_no_of_support === completed + closed + rejected ){
        frm.doc.overall_status = 'Completed'
      }else{
        frm.doc.overall_status = 'Partially completed'
      }
    }

  },
  onupdate:function(frm){
    // console.log("after save " , frm)
  },
  refresh(frm) {
    global_data.push(frm.selected_doc.support_table)
    var parentField = frm.fields_dict['family'];
    if(frm.doc.head_of_family){
      parentField.df.hidden = 1;
      parentField.refresh();
    }
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
        frm.fields_dict["district_of_origin"].get_query = function (doc) {
            return {
              filters: {
                State: "please select Current state",
              },
            };
          }
        frm.fields_dict["block_of_origin"].get_query = function (doc) {
            return {
              filters: {
                District: "please select Current district",
              },
            };
          }

// DEFULTS DATE SET 
          frm.set_value('registration_date', frappe.datetime.get_today());
	},
  state_of_origin: function(frm){
    frm.fields_dict["district_of_origin"].get_query = function (doc) {
      return {
        filters: {
          State: frm.doc.state_of_origin,
        },
      };
    }
    // clear dependent dropdowns values
    frm.set_value('block_of_origin', '')
    frm.set_value('block_of_origin', '')
  },
  district_of_origin: function(frm){
    frm.fields_dict["block_of_origin"].get_query = function (doc) {
      return {
        filters: {
          District: frm.doc.district_of_origin,
        },
      };
    }
    frm.set_value('block_of_origin', '')
  },

  do_you_have_id_document: function(frm){
    console.log("Form data",frm.doc)
      var id_section = frm.get_field('id_section');
        if (frm.doc.do_you_have_id_document === 'Yes') {
            id_section.df.hidden = 0;
            id_section.refresh();
        } else {
            id_section.df.hidden = 1;
            id_section.refresh();
  }
  },
  head_of_family:function(frm){
    var parentField = frm.fields_dict['family'];
    if(frm.doc.head_of_family){
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
  },
  // support_tab_add:function(frm){
  //   console.log("support add")
  //   frm.fields_dict['specific_support_type'].grid.get_field('specific_support_type').get_query = function(doc , cdt , cdn){
  //     return {
  //       filters: [
  //           ['support_type', '=', supportType], // Add your filter conditions
  //       ],
  //   };
  //   }
  // }
  
});
// ********************* SUPERT CHILD Table***********************
frappe.ui.form.on('Support Child', {
  form_render(frm){
    console.log("global_data",global_data)
  },
  
  refresh(frm){},
  status:function(frm, cdt, cdn){
    let row = frappe.get_doc(cdt, cdn);
    let status = row.status
    // frappe.model.set_value(cdt, cdn, 'reason_of_rejection', 1);
    // row.reason_of_rejection = 1
    if(status ==="Rejected"){
      row.reason_of_rejection = 0
    }
    frm.refresh_field('support_tab');
  },
  support_table_add(frm, cdt, cdn) {
      let row = frappe.get_doc(cdt, cdn);
    
  },
  
  support_type:function(frm , cdt , cdn){
    console.log("cd,cdn", cdt , cdn)
    let row = frappe.get_doc(cdt, cdn);
    let supportType = row.support_type;


  frm.refresh_field('support_table');
  }
})
// ********************* FOLLOW UP CHILD Table***********************
frappe.ui.form.on('Follow Up Child', {
  followup_table_add(frm, cdt, cdn) {
    let row = frappe.get_doc(cdt, cdn);
    console.log( frm.fields_dict.followup_table)
    // frm.set_value(frm.fields_dict.followup_table[0].follow_up_status, "Closed")
    console.log("child frm",row)
    // frappe.meta.get_docfield("Follow Up Child", "support_name",
		// cur_frm.support_name).options = "Initial\n1 Month\n2 Months\n3 Months\n6 Months";
		// refresh_field("support_name");
    // row.support_name='support_name';
    // frm.set_field_options('support_name', 'Option Value');
    // frm.set_df_property('support_name', 'options', '[aaa]');
    // frm.refresh_field('support_name');\
    
  },
})
