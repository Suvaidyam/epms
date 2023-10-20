import frappe
from epms.utils.cache import Cache
class  Filter:
    def set_report_filters(filters = None, date_column='creation'):
        new_filters = {}
        if filters is None:
            return new_filters
        if filters.from_date and filters.to_date:
            new_filters[date_column]= ["between", [filters.from_date, filters.to_date]]
        elif filters.from_date:
            new_filters[date_column]=[">=", filters.from_date]
        elif filters.to_date:
            new_filters[date_column]=["<=", filters.to_date]

        for filter_key in filters:
            if filter_key not in ['from_date','to_date']:
                new_filters[filter_key] = filters[filter_key]

        csc = None
        user = frappe.session.user
        if "MIS executive" in frappe.get_roles(user) and ("Administrator" not in frappe.get_roles(user)):
            csc = Cache.get_csc()
            new_filters["csc"] = csc

        return new_filters