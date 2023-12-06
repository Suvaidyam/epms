import frappe
from epms.utils.cache import Cache
def list_query(user):
    if not user:
        user = frappe.session.user
        
        # return """(`tabUser`.csc = '{0}')""".format(value)
    return ""
