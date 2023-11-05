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
    freeze_message: __("Calling"),
    callback: async function(response) {
      frm.fields_dict.support_table.grid.update_docfield_property("specific_support_type","options", response.results);
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
    freeze_message: __("Calling"),
    callback: async function(response) {
      frm.fields_dict.support_table.grid.update_docfield_property("support_type","options", response.results);
    }}); 
};
// ///////////////////////////////////////////////////////////////////////
function bank_name(frm,data=[]){
  var new_bank = frm.fields_dict['other_bank_account'];
  for(a of data){
    if(a.bank_name==="Others"){
      new_bank.df.hidden = 0;
      frm.set_df_property('other_bank_account', 'reqd', 1);
      new_bank.refresh();
    }else{
      new_bank.df.hidden = 1;
      frm.set_df_property('other_bank_account', 'reqd', 0);
      new_bank.refresh();
    }
  }
}

// /////////////////////////////////////////////////////////////////////////
frappe.ui.form.on("Beneficiary", {
  before_save: function (frm) {
    // follow up status manage
    if (frm.selected_doc.followup_table) {
      for (follow_up_items of frm.selected_doc.followup_table) {
        let support_name = follow_up_items.support_name;
        for (support_items of frm.selected_doc.support_table) {
          if (support_items.specific_support_type === support_name) {
            if (follow_up_items.follow_up_status === "Not interested") {
              support_items.status = "Closed"
            } else if (follow_up_items.follow_up_status === "Interested") {
              // support_items.status = "Open"
              if (support_items.status === 'Closed') {
                support_items.status = "Open"
              }
            } else {
              support_items.status = follow_up_items.follow_up_status
            }
          }
        }
      }
    }

    // console.log("before save ", frm.selected_doc.support_table)
    let open, under_process, form_submitted, rejected, completed, closed;
    open = under_process = form_submitted = rejected = completed = closed = 0;
    let total_no_of_support = 0
    if (frm.selected_doc.support_table) {
      for (item of frm.selected_doc.support_table) {
        // global_data.push(item)
        ++total_no_of_support
        if (item.status === 'Open') {
          ++open
        } else if (item.status === 'Under process') {
          ++under_process
        } else if (item.status === 'Form submitted') {
          ++form_submitted
        } else if (item.status === 'Rejected') {
          ++rejected
        } else if (item.status === 'Completed') {
          ++completed
        } else {
          ++closed
        }
      }
    }
    let numberic_overall_status = (completed + rejected) + '/' + (completed + rejected + form_submitted + under_process + open)
    // console.log(open , under_process,form_submitted , rejected , completed)
    frm.doc.numeric_overall_status = numberic_overall_status;
    // console.log(numberic_overall_status , total_no_of_support)
    if (total_no_of_support === open) {
      frm.doc.overall_status = 'Open'
    } else if (total_no_of_support === completed) {
      frm.doc.overall_status = 'Completed'
    } else {
      if (total_no_of_support === open + under_process + form_submitted) {
        frm.doc.overall_status = 'Open'
      } else if (total_no_of_support === completed + closed + rejected) {
        frm.doc.overall_status = 'Completed'
      } else {
        frm.doc.overall_status = 'Partially completed'
      }
    }
  },
  onupdate: function (frm) {
    // console.log("after save " , frm)
  },
  refresh(frm) {
    // hide advance search and create new option in lists
    frm.set_df_property('current_location', 'only_select', true);
    frm.set_df_property('occupation', 'only_select', true);
    frm.set_df_property('existing_bank_account', 'only_select', true);
    frm.set_df_property('state_of_origin', 'only_select', true);
    frm.set_df_property('district_of_origin', 'only_select', true);
    frm.set_df_property('block_of_origin', 'only_select', true);
    frm.set_df_property('caste', 'only_select', true);
    frm.set_df_property('source_information_about_center', 'only_select', true);
    frm.set_df_property('education', 'only_select', true);
    frm.set_df_property('family', 'only_select', true);
    frm.set_df_property('education', 'only_select', true);

    let parentField = frm.fields_dict['family'];
    if (frm.doc.head_of_family === 'Yes') {
      parentField.df.hidden = 0;
      parentField.refresh();
    }else{
      parentField.df.hidden = 1;
      parentField.refresh();
    }
    let new_occupation = frm.fields_dict['new_occupation'];
    if (frm.doc.occupation === "Others") {
      frm.set_df_property('new_occupation', 'reqd', 1);
      new_occupation.df.hidden = 0;
      new_occupation.refresh();
    } else {
      frm.set_df_property('new_occupation', 'reqd', 0);
    }
    bank_name(frm,frm.doc.existing_bank_account)

    var have_bank = frm.fields_dict['existing_bank_account'];
    if (frm.doc.do_you_have_bank_account === "Yes") {
      have_bank.df.hidden = 0;
      frm.set_df_property('existing_bank_account', 'reqd', 1);
      have_bank.refresh();
    } else {
      have_bank.df.hidden = 1;
      frm.set_df_property('existing_bank_account', 'reqd', 0);
      have_bank.refresh();
    }

    let new_location = frm.fields_dict['other_current_location'];
    if (frm.doc.current_location === "Others") {
      frm.set_df_property('other_current_location', 'reqd', 1);
      new_location.df.hidden = 0;
      new_location.refresh();
    } else {
      frm.set_df_property('other_current_location', 'reqd', 0);
    }
    let new_sorce = frm.fields_dict['other_source_information_about_center'];
    if (frm.doc.source_information_about_center === "Others") {
      frm.set_df_property('other_source_information_about_center', 'reqd', 1);
      new_sorce.df.hidden = 0;
      new_sorce.refresh();
    } else {
      frm.set_df_property('other_source_information_about_center', 'reqd', 0);
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
    if(frm.doc.__islocal){
      frm.set_value('registration_date', frappe.datetime.get_today());
    }
  },
  setup(frm) {
    frm.set_query("current_location", () => {
      return { "query": "select name from `tabCurrent location` order by sequence asc , name asc"  };
    });
    frm.set_query("occupation", () => {
      return { "query": "select name from `tabCurrent Occupation` order by sequence asc , name asc" };
    });
    frm.set_query("existing_bank_account", () => {
      return { "query": "select name from `tabBank` order by sequence asc, name asc" };
    });
    frm.set_query("state_of_origin", () => {
      return { page_length: 1000 };
    });

    frm.set_query("caste", () => {
      return { "query": "select name from `tabCaste master` order by sequence asc , name asc" };
    });
    frm.set_query("source_information_about_center", () => {
      return {"query": "select name from `tabSource information about center` order by sequence asc , name asc" };
    });
    frm.set_query("education", () => {
      return {"query": "select name from `tabEducation master` order by sequence asc"};
    });
  },

  state_of_origin: function (frm) {
    frm.fields_dict["district_of_origin"].get_query = function (doc) {
      return {
        filters: {
          State: frm.doc.state_of_origin,
        },
        page_length: 1000
      };
    }
    // clear dependent dropdowns values
    frm.set_value('block_of_origin', '')
    frm.set_value('district_of_origin', '')
  },
  district_of_origin: function (frm) {
    frm.fields_dict["block_of_origin"].get_query = function (doc) {
      return {
        filters: {
          District: frm.doc.district_of_origin,
        },
        page_length: 1000 
      };
    }
    frm.set_value('block_of_origin', '')
  },

  do_you_have_id_document: function (frm) {
    var id_section = frm.get_field('id_section');
    if (frm.doc.do_you_have_id_document === 'Yes') {
      id_section.df.hidden = 0;
      id_section.refresh();
    } else {
      id_section.df.hidden = 1;
      id_section.refresh();
    }
  },
  head_of_family: function (frm) {
    var parentField = frm.fields_dict['family'];
    if (frm.doc.head_of_family === "No" || frm.doc.head_of_family ==='') {
      parentField.df.hidden = 1;
      frm.set_df_property('family', 'reqd', 0);
      parentField.refresh();
    } else {
      parentField.df.hidden = 0;
      frm.set_df_property('family', 'reqd', 1);
      parentField.refresh();
    }
  },
  do_you_have_bank_account: function (frm) {
    var have_bank = frm.fields_dict['existing_bank_account'];
    if (frm.doc.do_you_have_bank_account === "Yes") {
      have_bank.df.hidden = 0;
      frm.set_df_property('existing_bank_account', 'reqd', 1);
      have_bank.refresh();
    } else {
      have_bank.df.hidden = 1;
      frm.set_df_property('existing_bank_account', 'reqd', 0);
      have_bank.refresh();
    }
  },
  date_of_birth: function (frm) {
    let dob = frm.doc.date_of_birth
    if (dob) {
      let year = frappe.datetime.get_today()
      let age = year.split('-')[0] - dob.split('-')[0]
      frm.set_value('age', age)
      frm.set_df_property('age', 'read_only', 1);
    } else {
      frm.set_df_property('age', 'read_only', 0);
      frm.set_value('age', null)
    }
  },
  occupation: function (frm) {
    var new_occupation = frm.fields_dict['new_occupation'];
    if (frm.doc.occupation === "Others") {
      new_occupation.df.hidden = 0;
      frm.set_df_property('new_occupation', 'reqd', 1);
      new_occupation.refresh();
    } else {
      new_occupation.df.hidden = 1;
      frm.set_df_property('new_occupation', 'reqd', 0);
      new_occupation.refresh();
    }
  },
  existing_bank_account: function (frm) {
    // Call function on top
    bank_name(frm,frm.doc.existing_bank_account)
  },
  current_location: function (frm) {
    var new_location = frm.fields_dict['other_current_location'];
    if (frm.doc.current_location === "Others") {
      frm.set_df_property('other_current_location', 'reqd', 1);
      new_location.df.hidden = 0;
      new_location.refresh();
    } else {
      new_location.df.hidden = 1;
      frm.set_df_property('other_current_location', 'reqd', 0);
      new_location.refresh();
    }
  },
  source_information_about_center: function (frm) {
    var new_sorce = frm.fields_dict['other_source_information_about_center'];
    if (frm.doc.source_information_about_center === "Others") {
      frm.set_df_property('other_source_information_about_center', 'reqd', 1);
      new_sorce.df.hidden = 0;
      new_sorce.refresh();
    } else {
      new_sorce.df.hidden = 1;
      frm.set_df_property('other_source_information_about_center', 'reqd', 0);
      new_sorce.refresh();
    }
  },
  


});
// ********************* SUPERT CHILD Table***********************
frappe.ui.form.on('Support Child', {

  refresh(frm) {
    frm.set_query("specific_support_type", () => {
      return { page_length: 1000 };
    });
  },
  specific_support_type: function (frm) {
    frm.set_query("specific_support_type", () => {
      return { page_length: 1000 };
    });
  },
  support_table_add(frm, cdt, cdn) {
    let row = frappe.get_doc(cdt, cdn);
    get_support_types(frm)
    // set_field_options("specific_support_type", ["Loan Approved","Loan Appealing"])

  },
  support_type: function (frm, cdt, cdn) {
    let row = frappe.get_doc(cdt, cdn);
    // console.log("row", row)
    get_support_list(frm,row.support_type)
    // frm.fields_dict.support_table.grid.update_docfield_property("specific_support_type","options",["Loan Approved","Loan Appealing"]);

  }
})
// ********************* FOLLOW UP CHILD Table***********************
frappe.ui.form.on('Follow Up Child', {
  followup_table_add(frm, cdt, cdn) {
    let row = frappe.get_doc(cdt, cdn);
      let support_data = []
      for(support_name of frm.doc.support_table){
        if(support_name.status != "Closed"){
          support_data.push(support_name.specific_support_type)
        }
      }

    frm.fields_dict.followup_table.grid.update_docfield_property("support_name","options", support_data);

  },
})


