import frappe
from epms.utils.cache import Cache
def list_query(user):
    if not user:
        user = frappe.session.user
    
    if( "Administrator" not in frappe.get_roles(user)):
        profile_condition = f"""(`tabUser`.name = '{user}' OR `tabUser`.role_profile_name = 'MIS executive')"""
        # return """(`tabUser`.role_profile_name = 'MIS executive')"""
        return profile_condition
    else:
        return ""
