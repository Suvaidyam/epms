import frappe

def allocate_csc(login_manager):
    user = frappe.get_doc("User", frappe.session.user)
    frappe.session['csc_centre'] = user.csc
    frappe.msgprint(("Welcome, {0}! Your session has been created.".format(frappe.session)))
    return "Session updated successfully"


