import frappe
def list_query(user):
    if not user:
        user = frappe.session.user
    print(user)
    # todos that belong to user or assigned by user
    return ""
    #return "(`tabBeneficiary`.csc = 'CSC-S07097-002')"
