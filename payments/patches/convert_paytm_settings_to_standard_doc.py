import frappe
from payments.utils import erpnext_app_import_guard
from frappe.utils.password import get_decrypted_password

def execute():
	with erpnext_app_import_guard():
		from erpnext import get_default_company
		
	if not get_default_company():
		return

	mandatory_fields = ["merchant_id", "merchant_key"]
	existing_values = frappe.db.get_singles_dict("Paytm Settings")

	if not existing_values:
		return

	if not all(existing_values.get(field) for field in mandatory_fields):
		return

	if frappe.db.count("Paytm Settings") > 0:
		return

	frappe.get_doc({
		"doctype": "Paytm Settings",
		"payment_gateway_name" : existing_values['merchant_id'],
		"merchant_id": existing_values["merchant_id"],
		"merchant_key": get_decrypted_password("Paytm Settings", "Paytm Settings", "merchant_key"),
		"staging": existing_values.get("staging"),
		"industry_type_id": existing_values.get("industry_type_id"),
		"website": existing_values.get("website"),
		"company": get_default_company(),
	}).insert(ignore_if_duplicate=True)