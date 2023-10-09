import frappe
def list_query(user):
    if not user:
        user = frappe.session.user
    print(user)
    user = frappe.get_doc("User", frappe.session.user)
    # frappe.session['csc_centre'] = user.csc
    # todos that belong to user or assigned by user
    # return frappe.msgprint(format(frappe.session))
    # return ""
    # return "(`tabBeneficiary`.csc = user.csc)"
    
    return """(`tabBeneficiary`.csc = '{0}')""".format(user.csc)
    # if "System Manager" in frappe.get_roles(user):
    #     # System Managers have full access
    #     return ""

    # return """(`tabBeneficiary`.csc = '{0}')""".format(user.csc)
