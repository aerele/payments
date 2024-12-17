import frappe
from payments.utils import erpnext_app_import_guard
from frappe.utils.password import get_decrypted_password

def execute():
    with erpnext_app_import_guard():
        from erpnext import get_default_company

    if not get_default_company():
        return

    mandatory_fields = ["api_username", "api_password", "signature"]
    existing_values = frappe.db.get_singles_dict("PayPal Settings")

    if not existing_values:
        return
    
    if not all(existing_values.get(field) for field in mandatory_fields):
        return
    
    if frappe.db.count("PayPal Settings") > 0:
        return
    
    frappe.get_doc({
		"doctype": "PayPal Settings",
		"payment_gateway_name" : existing_values['api_username'],
		"api_username": existing_values["api_username"],
		"api_password": get_decrypted_password("PayPal Settings", "PayPal Settings", "api_password"),
		"signature": existing_values.get("signature"),
		"paypal_sandbox": existing_values.get("paypal_sandbox"),
		"redirect_to": existing_values.get("redirect_to"),
		"company": get_default_company(),
	}).insert(ignore_if_duplicate=True)
