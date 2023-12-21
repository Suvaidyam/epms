import frappe
# from epms.utils.cache import Cache
def list_query(user):
    if not user:
        user = frappe.session.user
        
    if "Admin" in frappe.get_roles(user) and ("Administrator" not in frappe.get_roles(user)):
        return """(`tabRole Profile`.role_profile = '{0}')""".format('MIS executive')
    # System Managers have full access
    return ""
