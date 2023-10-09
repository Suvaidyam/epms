import frappe

def allocate_csc(login_manager):
    
    if "MIS executive" in frappe.get_roles(frappe.session.user) and ("Administrator" not in frappe.get_roles(frappe.session.user)):
        user = frappe.get_doc("User", frappe.session.user)
        frappe.cache().set_value('csc-'+user.name, user.csc)


