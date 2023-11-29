import frappe
from epms.utils.cache import Cache

class Primary_member:
    def create_family(beneficiary):
        if beneficiary:
            family_doc = frappe.new_doc("Primary Member")
            family_doc.head_of_family = beneficiary.name
            family_doc.name_of_parents = beneficiary.name_of_the_beneficiary
            family_doc.contact_number = beneficiary.contact_number
            family_doc.csc = Cache.get_csc()
            family_doc.insert()
            return family_doc
        else:
            return frappe.printmsg("New Beneficary Not Found")
    
    def update_family(beneficiary):
        family_doc_name = frappe.get_list("Primary Member",
        filters={'head_of_family': beneficiary.name},
        fields=["name"])
        if(family_doc_name):
            family_doc = frappe.get_doc("Primary Member", family_doc_name[0].name)
            family_doc.name_of_parents = beneficiary.name_of_the_beneficiary
            family_doc.contact_number = beneficiary.contact_number
			# family_doc.csc = beneficiary.csc
            family_doc.save()
        else:
            family_doc = frappe.new_doc("Primary Member")
            family_doc.head_of_family = beneficiary.name
            family_doc.name_of_parents = beneficiary.name_of_the_beneficiary
            family_doc.contact_number = beneficiary.contact_number
            family_doc.csc = beneficiary.csc
            family_doc.insert()
			# update current beneficery to family
            frappe.msgprint("New Beneficary Update As a Head of Family")
        return family_doc
    
    def delete_family(beneficiary):


        delate_family = frappe.db.delete("Primary Member", {
                        "name": beneficiary.contact_number})   
        return delate_family