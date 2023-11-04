import frappe
from frappe import _

@frappe.whitelist()
def get_support_list(support_type = None):
    # Query the database to fetch the list
    if support_type:
       query = f"SELECT name FROM `tabSupport` WHERE support_type = '{support_type}'"
    else:
        query = f"SELECT name FROM `tabSupport`"

    support = frappe.db.sql(query , as_dict=True)
    support_tuple = tuple(row["name"] for row in support)

    return support_tuple
