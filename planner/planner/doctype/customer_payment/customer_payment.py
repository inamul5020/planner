# Copyright (c) 2025, YOUR COMPANY / NAME and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class CustomerPayment(Document):
	def on_submit(self):
		"""
		This method is a 'hook' that is automatically called by Frappe
		when a Customer Payment document is submitted.
		"""
		# Check if a customer is linked to this payment
		if self.customer:
			try:
				# Get the full customer document from the database
				customer = frappe.get_doc("Customer", self.customer)
				
				# Subtract the payment amount from the customer's balance
				customer.balance_total -= self.amount
				
				# Save the updated customer document
				# ignore_permissions=True is important for server-side scripts
				customer.save(ignore_permissions=True)
				
				# Add a success message for the user in the UI
				frappe.msgprint(f"Customer {self.customer}'s balance updated successfully.")

			except Exception as e:
				# If something goes wrong, show an error message
				frappe.throw(f"An error occurred while updating the customer balance: {e}")