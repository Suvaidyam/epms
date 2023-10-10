import frappe
def list_query(user):
    if not user:
        user = frappe.session.user
        
    if "MIS executive" in frappe.get_roles(user) and ("Administrator" not in frappe.get_roles(user)):
        value = frappe.cache().get_value("csc-"+user)
        # frappe.msgprint("csc"+(value))
        return """(`tabPrimary Member`.csc = '{0}')""".format(value)
    # System Managers have full access
    return ""
