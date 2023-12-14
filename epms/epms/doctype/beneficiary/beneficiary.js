// Copyright (c) 2023, Management System for Agrasarteach@suvaidyam.com and contributors
// For license information, please see license.txt
const dialogsConfig = {
  document_submitted: {
    title: 'Enter details for Support',
    fields: [
      {
        label: 'Date of application',
        fieldname: 'date_of_application',
        fieldtype: 'Date',
        reqd: 1,
        _doc: true
      },
      {
        label: 'Application number',
        fieldname: 'application_number',
        fieldtype: 'Data',
        _doc: true
      },
      {
        label: 'Amount paid',
        fieldname: 'amount_paid',
        fieldtype: 'Int',
        _doc: true
      },
      {
        label: 'Paid by',
        fieldname: 'paid_by',
        fieldtype: 'Select',
        options: ["Self", "CSC"],
        _doc: true
      }
    ]
  },
  document_completed: {
    title: 'Enter details for Support',
    fields: [
      {
        label: 'Date of completion',
        fieldname: 'date_of_completion',
        fieldtype: 'Date',
        reqd: 1,
        _doc: true
      },
      {
        label: 'Completion certificate',
        fieldname: 'completion_certificate',
        fieldtype: 'Attach',
        _doc: true
      }
    ]
  },
  document_rejected: {
    title: 'Enter details for Support',
    fields: [
      {
        label: 'Date of rejection',
        fieldname: 'date_of_rejection',
        fieldtype: 'Date',
        reqd: 1,
        _doc: true
      },
      {
        label: 'Reason of rejection',
        fieldname: 'reason_of_rejection',
        fieldtype: 'Data',
        _doc: true
      }
    ]
  }
}
const createDialog = (_doc, config) => {
  return new frappe.ui.Dialog({
    title: config.title,
    fields: config.fields,
    size: 'small', // small, large, extra-large
    primary_action_label: 'Save',
    primary_action(obj) {
      let fields = config.fields.filter(f => f._doc).map(e => e.fieldname)
      for (let field of fields) {
        if (obj[field])
          _doc[field] = obj[field]
      }
      console.log("config", config.title, _doc);
      this.hide()
    }
  });
}
////////////////////////////////
function get_support_list(frm, support_type) {
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
    freeze: true,
    freeze_message: __("Calling"),
    callback: async function (response) {
      let under_process_completed_ops = frm.doc.support_table.filter(f => (['Under process', 'Open', 'Closed'].includes(f.status))).map(m => m.specific_support_type)
      // console.log("under_process_completed_ops", under_process_completed_ops)
      let ops = response?.results?.filter(f => !under_process_completed_ops.includes(f.value))
      // console.log(" options", ops)
      frm.fields_dict.support_table.grid.update_docfield_property("specific_support_type", "options", ops);
    }
  });
};
// //////////////////////////////////////////////////////////////////////
function get_support_types(frm) {
  frappe.call({
    method: 'frappe.desk.search.search_link',
    args: {
      doctype: 'Support Type',
      txt: '',
      page_length: 100,  // Adjust the number of results per page as needed
    },
    freeze: true,
    freeze_message: __("Calling"),
    callback: async function (response) {
      frm.fields_dict.support_table.grid.update_docfield_property("support_type", "options", response.results);
      console.log(response)
    }
  });
};
// ///////////////////////////////////////////////////////////////////////
function bank_name(frm, data = []) {
  var new_bank = frm.fields_dict['other_bank_account'];
  //  filter data from delected field and run conditions
  let ops = data?.filter(f => ['Others'].includes(f.bank_name))
  if (ops[0]?.bank_name == "Others") {
    new_bank.df.hidden = 0;
    frm.set_df_property('other_bank_account', 'reqd', 1);
    new_bank.refresh();
  } else {
    frm.doc.other_bank_account = ''
    new_bank.df.hidden = 1;
    frm.set_df_property('other_bank_account', 'reqd', 0);
    new_bank.refresh();
  }

}
// disable checkbxes
function controlChildTable(frm, options = { disableCheckbox: true }) {
  return;
  let childTables = ['support_table', 'followup_table']
  for (let table of childTables) {
    let rows = frm.fields_dict[table].grid.grid_rows;
    for (row of rows) {
      if (!row.doc.__islocal) {
        if (options.disableCheckbox) {
          let checkboxElement = $(row.row_check).find('input[type="checkbox"]');
          setTimeout(() => {
            checkboxElement.prop('disabled', true)
          }, 500);
        }
      }

    }
  }
  // frm.refresh()
}

// /////////////////////////////////////////////////////////////////////////
frappe.ui.form.on("Beneficiary", {
  after_save: () => {
    // window.location.reload();
  },
  validate: function (frm) {
    if (frm.doc.do_you_have_id_document == "Yes" && frm.doc.id_section?.length == '0') {
      if (!(frm.doc.id_section[0] && frm.doc?.id_section[0]?.select_id != "undefined")) {
        frappe.throw('Please Select Which of the following ID documents do you have?');
      }
      return
    }
    console.log("frm.selected_doc.support_table", frm.selected_doc.support_table);
    // support status manage
    if (frm.selected_doc.support_table) {
      for (support_items of frm.selected_doc.support_table) {
        if (support_items.application_submitted == "No") {
          support_items.status = 'Open'
        } else if (support_items.application_submitted == "Yes") {
          support_items.status = 'Under process'
        } else {
          support_items.status = 'Completed'
        }
      }
    }
    // follow up status manage
    if (frm.selected_doc.followup_table) {
      for (support_item of frm.selected_doc.support_table) {
        if (!['Completed'].includes(support_item.status)) {
          let followups = frm.selected_doc.followup_table.filter(f => f.parent_ref == support_item?.name)
          let latestFollowup = followups.length ? followups[(followups.length - 1)] : null
          if (latestFollowup) {
            switch (latestFollowup.follow_up_status) {
              case "Interested":
                support_item.status = "Open"
                break;
              case "Not interested":
                support_item.status = "Closed"
                break;
              case "Rejected":
                support_item.status = "Rejected"
                support_item.date_of_rejection = latestFollowup.date_of_rejection || support_item.date_of_rejection
                support_item.reason_of_rejection = latestFollowup.reason_of_rejection || support_item.reason_of_rejection
                break;
              case "Document submitted":
                support_item.application_submitted = "Yes"
                support_item.status = "Under process"
                support_item.date_of_application = latestFollowup.date_of_application || support_item.date_of_application
                support_item.application_number = latestFollowup.application_number || support_item.application_number
                support_item.amount_paid = latestFollowup.amount_paid || support_item.amount_paid
                support_item.paid_by = latestFollowup.paid_by || support_item.paid_by
                break;
              case "Completed":
                support_item.status = "Completed"
                support_item.date_of_completion = latestFollowup.date_of_completion || support_item.date_of_completion
                support_item.completion_certificate = latestFollowup.completion_certificate || support_item.completion_certificate
                break;
              case "Not reachable":
                support_item.status = support_item?.application_submitted == "Yes" ? "Under process" : "Open"
                if(latestFollowup.to_close_status){
                  support_item.status = latestFollowup.to_close_status
                }
                break;
              default:
                support_item.status = "Under process"
                break;
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
    console.log("frm.selected_doc.support_table", frm.selected_doc.support_table);

    // frm.fields_dict['support_table'].grid.refresh();
    // window.location.reload();
  },
  onupdate: function (frm) {
    // frm.refresh()
  },
  refresh(frm) {
    // child table api defult call
    get_support_types(frm)
    console.log(frm.doc?.support_table)
    if (frm.doc.support_table) {
      get_support_list(frm, cur_frm.doc?.support_table[0]?.support_type)
    }

    // console.log("frappe.session.user", frappe.session.user)
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
    } else {
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
    bank_name(frm, frm.doc.existing_bank_account)

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
    if (frm.doc?.current_location?.split('-')[0] === "Others") {
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
    if (!frappe.user_roles.includes("MIS executive") || frappe.user_roles.includes("Administrator")) {
      if (frm.doc.csc) {
        frm.fields_dict["current_location"].get_query = function (doc) {
          return {
            filters: {
              centre: frm.doc.csc,
            },
            page_length: 1000
          };
        }
      } else {
        frm.fields_dict["current_location"].get_query = function (doc) {
          return {
            filters: {
              centre: "please select Center",
            },
            page_length: 1000
          };
        }
      }
    }
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
    if (frm.doc.__islocal) {
      frm.set_value('registration_date', frappe.datetime.get_today());
    }
    controlChildTable(frm)
  },
  setup(frm) {
    frm.set_query("current_location", () => {
      // return { "query": "select name from `tabCurrent location` order by sequence asc , name asc"  };
      return { page_length: 1000 };
    });
    frm.set_query("occupation", () => {
      // return { "query": "select name from `tabCurrent Occupation` order by sequence asc , name asc" };
      return { page_length: 1000 };
    });
    frm.set_query("existing_bank_account", () => {
      // return { "query": "select name from `tabBank` order by sequence asc, name asc" };
      return { page_length: 1000 };
    });
    frm.set_query("state_of_origin", () => {
      return { page_length: 1000 };
    });

    frm.set_query("caste", () => {
      return { "query": "select name from `tabCaste master` order by sequence asc , name asc" };
    });
    frm.set_query("source_information_about_center", () => {
      return { "query": "select name from `tabSource information about center` order by sequence asc , name asc" };
    });
    frm.set_query("education", () => {
      return { "query": "select name from `tabEducation master` order by sequence asc" };
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
      frm.doc.id_section = []
      id_section.df.hidden = 1;
      id_section.refresh();
    }
  },
  head_of_family: function (frm) {
    var parentField = frm.fields_dict['family'];
    if (frm.doc.head_of_family === "No" || frm.doc.head_of_family === '') {
      parentField.df.hidden = 1;
      frm.set_df_property('family', 'reqd', 0);
      frm.doc.family = ""
      parentField.refresh();
    } else {
      parentField.df.hidden = 0;
      frm.set_df_property('family', 'reqd', 1);
      frm.doc.family = ""
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
    bank_name(frm, frm.doc.existing_bank_account)
  },
  current_location: function (frm) {
    var new_location = frm.fields_dict['other_current_location'];
    if (frm.doc.current_location.split('-')[0] === "Others") {
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
  csc: function (frm) {
    frm.fields_dict["current_location"].get_query = function (doc) {
      return {
        filters: {
          centre: frm.doc.csc,
        },
        page_length: 1000
      };
    }
  }



});
// ********************* Support CHILD Table***********************
frappe.ui.form.on('Support Child', {

  refresh(frm) {
    // specific_support_type
    // status != ['']
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
    controlChildTable(frm)
    // set_field_options("specific_support_type", ["Loan Approved","Loan Appealing"])

  },
  support_type: function (frm, cdt, cdn) {
    let row = frappe.get_doc(cdt, cdn);
    // console.log("row", row)
    get_support_list(frm, row.support_type)
    // frm.fields_dict.support_table.grid.update_docfield_property("specific_support_type","options",["Loan Approved","Loan Appealing"]);

  },
  application_submitted: function (frm, cdt, cdn) {
    let row = frappe.get_doc(cdt, cdn);
    if(row.application_submitted == "Yes"){
      createDialog(row, dialogsConfig.document_submitted).show();
    }else if(row.application_submitted == "Completed"){
      createDialog(row, dialogsConfig.document_completed).show();
    }
  }

})
// ********************* FOLLOW UP CHILD Table***********************
frappe.ui.form.on('Follow Up Child', {
  followup_table_add(frm, cdt, cdn) {
    let row = frappe.get_doc(cdt, cdn);
    let support_data = frm.doc.support_table.filter(f => (f.status != 'Completed' && f.status != 'Rejected' && !f.__islocal)).map(m => m.specific_support_type);
    row.follow_up_date = frappe.datetime.get_today()
    frm.fields_dict.followup_table.grid.update_docfield_property("support_name", "options", support_data);
  },
  support_name: function (frm, cdt, cdn) {
    let row = frappe.get_doc(cdt, cdn);
    console.log("frm.doc.support_table:", frm.doc.support_table);
    let supports = frm.doc.support_table.filter(f => f.specific_support_type == row.support_name);
    let latestSupport = supports.length ? supports[supports.length - 1] : null;
    if (latestSupport) {
      row.parent_ref = latestSupport.name
    }
    for (support_items of frm.doc.support_table) {
      if (row.support_name == support_items.specific_support_type) {
        console.log(support_items.specific_support_type)
        console.log(support_items)
        if (support_items.status === "Open" && support_items.application_submitted == "No") {
          frm.fields_dict.followup_table.grid.update_docfield_property("follow_up_with", "options", ["Beneficiary"]);
          row.follow_up_with = "Beneficiary"
          frm.fields_dict.followup_table.grid.update_docfield_property("follow_up_status", "options", ["Interested", "Not interested", "Document submitted", "Not reachable"]);
        } else if (support_items.status === "Under process" && support_items.application_submitted == "Yes") {
          frm.fields_dict.followup_table.grid.update_docfield_property("follow_up_with", "options", ["Beneficiary", "Government department", "Government website", "Others"]);
          frm.fields_dict.followup_table.grid.update_docfield_property("follow_up_status", "options", ["Not reachable", "Under process", "Additional info required", "Completed", "Rejected"]);
        }else if (support_items.status === "Closed" && support_items.application_submitted == "Yes"){
          // last call update 
          frm.fields_dict.followup_table.grid.update_docfield_property("follow_up_with", "options", ["Beneficiary"]);
          frm.fields_dict.followup_table.grid.update_docfield_property("follow_up_status", "options", ["Not reachable", "Under process", "Additional info required", "Completed", "Rejected"]);
        }
      }
    }
  },
  follow_up_with: function (frm, cdt, cdn) {
    let row = frappe.get_doc(cdt, cdn);

    if (row.follow_up_with != "Beneficiary") {
      frm.fields_dict.followup_table.grid.update_docfield_property("follow_up_status", "options", ["Under process", "Additional info required", "Completed", "Rejected"]);
    }else{
      frm.fields_dict.followup_table.grid.update_docfield_property("follow_up_status", "options", ["Not reachable", "Under process", "Additional info required", "Completed", "Rejected"]);
    }
    //else {
    //   let support_data = frm.doc.support_table.filter(f => (f.status != 'Completed' && f.status != 'Rejected' && f.specific_support_type === row.support_name && !f.__islocal));
    //   // console.log(support_data[support_data.length - 1].status)
    //   if (support_data[support_data.length - 1].status === "Under process") {
    //     frm.fields_dict.followup_table.grid.update_docfield_property("follow_up_status", "options", ["Not reachable", "Under process", "Additional info required", "Completed", "Rejected"]);
    //   }
    // }
  },
  follow_up_status: function (frm, cdt, cdn) {
    let row = frappe.get_doc(cdt, cdn);
    let supports = frm.doc.support_table.filter(f => f.specific_support_type == row.support_name);
    let latestSupport = supports.length ? supports[supports.length - 1] : null;
    if (row.follow_up_status === "Document submitted") {
      createDialog(row, dialogsConfig.document_submitted).show();
      // dialog.show();
    } else if (row.follow_up_status === "Completed") {
      createDialog(row, dialogsConfig.document_completed).show();
      // document_completed.show()
    } else if (row.follow_up_status === "Rejected") {
      createDialog(row, dialogsConfig.document_rejected).show();
    } else if (row.follow_up_status === "Not reachable" && latestSupport.status != "Closed") {
      let followups = frm.doc.followup_table.filter(f => f.parent_ref == row.parent_ref && f.support_name == row.support_name && f.follow_up_status == "Not reachable")
      if (followups.length >= 2) {
        frappe.warn('Do you want to support the status?',
          `The follow-up status is "Not reachable" ${followups.length} times`,
          () => {
            row.to_close_status = "Closed"
            // console.log("aaaa", row)
          },
          'Close',
          true // Sets dialog as minimizable
        )

      }
      //  show popup and continue and close if more than two times
    }
  }
})


