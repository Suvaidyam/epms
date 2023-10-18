import frappe
from epms.utils.cache import Cache
def list_query(user):
    if not user:
        user = frappe.session.user
        
    if "MIS executive" in frappe.get_roles(user) and ("Administrator" not in frappe.get_roles(user)):
        value = Cache.get_csc()
        # frappe.msgprint("csc"+(value))
        return """(`tabBeneficiary`.csc = '{0}')""".format(value)
    # System Managers have full access
    return ""
