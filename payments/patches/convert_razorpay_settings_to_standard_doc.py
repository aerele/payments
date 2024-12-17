import frappe
from payments.utils import erpnext_app_import_guard
from frappe.utils.password import get_decrypted_password

def execute():
    with erpnext_app_import_guard():
        from erpnext import get_default_company
        
    if not get_default_company():
        return

    mandatory_fields = ["api_key", "api_secret"]
    existing_values = frappe.db.get_singles_dict("Razorpay Settings")

    if not existing_values:
        return
    
    if not all(existing_values.get(field) for field in mandatory_fields):
        return
    
    if frappe.db.count("Razorpay Settings") > 0:
        return
    
    frappe.get_doc({
		"doctype": "Razorpay Settings",
		"payment_gateway_name" : existing_values['api_key'],
		"api_key": existing_values["api_key"],
		"api_secret": get_decrypted_password("Razorpay Settings", "Razorpay Settings", "api_secret"),
		"redirect_to": existing_values.get("redirect_to"),
		"company": get_default_company(),
	}).insert(ignore_if_duplicate=True)
