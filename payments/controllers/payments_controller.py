import frappe
from frappe import _
from frappe.model.document import Document


class PaymentsController(Document):
    def validate_transaction_currency(self, currency):
        if currency not in self.supported_currencies:
            frappe.throw(
                _(
                    "Please select another payment method. Stripe does not support transactions in currency '{0}'"
                ).format(currency)
            )

    def create_payment_gateway(self):
	    # NOTE: we don't translate Payment Gateway name because it is an internal doctype
        if not frappe.db.exists("Payment Gateway", self.doctype.replace(" Settings", "-")+self.gateway_name):
            payment_gateway = frappe.get_doc(
                {
                    "doctype": "Payment Gateway",
                    "gateway": self.doctype.replace(" Settings", "-")+self.gateway_name,
                    "gateway_settings": self.doctype,
                    "gateway_controller": self.gateway_name,
                }
            )
            payment_gateway.insert(ignore_permissions=True)
