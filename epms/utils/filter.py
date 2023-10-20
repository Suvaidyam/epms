import frappe
from epms.utils.cache import Cache
class  Filter:
    def set_report_filters(filters = None, date_column='creation', str=False):
        new_filters = {}
        str_list = []
        if filters is None:
            return new_filters
        if filters.from_date and filters.to_date:
            if str:
                str_list.append(f"({date_column} between {filters.from_date} AND {filters.to_date})")
            else:
                new_filters[date_column]= ["between", [filters.from_date, filters.to_date]]
        elif filters.from_date:
            if str:
                str_list.append(f"({date_column} >= {filters.from_date})")
            else:
                new_filters[date_column]=[">=", filters.from_date]
        elif filters.to_date:
            if str:
                str_list.append(f"({date_column} <= {filters.to_date})")
            else:
                new_filters[date_column]=["<=", filters.to_date]

        for filter_key in filters:
            if filter_key not in ['from_date','to_date']:
                if str:
                    str_list.append(f"({filter_key}='{filters[filter_key]}')")
                else:
                    new_filters[filter_key] = filters[filter_key]

        csc = None
        user = frappe.session.user
        if "MIS executive" in frappe.get_roles(user) and ("Administrator" not in frappe.get_roles(user)):
            csc = Cache.get_csc()
            if str:
                str_list.append(f"(csc={csc})")
            else:
                new_filters["csc"] = csc
        if str:
            return ' AND '.join(str_list)
        else:
            return new_filters