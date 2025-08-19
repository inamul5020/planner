import os
import json
import frappe

# ANSI Colors
GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"

# --- Configuration ---
APP_NAME = "planner"

def log(msg, color=BLUE):
    """Prints a colored message to the console."""
    print(f"{color}{msg}{RESET}")

def run():
    """Entry point for the `bench execute` command."""
    log("="*40)
    log(f"Verifying DocTypes for app: {APP_NAME}...")

    try:
        app_path = frappe.get_app_path(APP_NAME)
        cfg_path = os.path.join(app_path, "doctypes.json")
    except frappe.exceptions.DoesNotExistError:
        log(f"❌ App '{APP_NAME}' not found.", RED)
        return

    if not os.path.exists(cfg_path):
        log(f"❌ doctypes.json not found in the '{APP_NAME}' app directory.", RED)
        return

    with open(cfg_path) as f:
        config = json.load(f)

    all_doctypes = config.get("order", [])
    if not all_doctypes:
        log("No DocTypes found in the 'order' list in doctypes.json.", RED)
        return

    found, not_found = [], []

    for doctype_name in all_doctypes:
        if frappe.db.exists("DocType", doctype_name):
            log(f"  ✅ Found: {doctype_name}", GREEN)
            found.append(doctype_name)
        else:
            log(f"  ❌ Not Found: {doctype_name}", RED)
            not_found.append(doctype_name)

    log("\nVerification Summary:")
    log(f"  Found: {len(found)}", GREEN)
    log(f"  Not Found: {len(not_found)}", RED)
    if not_found:
        log(f"  Missing DocTypes: {not_found}", RED)
    log("="*40)