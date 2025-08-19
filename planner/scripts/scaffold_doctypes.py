import os, json, frappe

# ANSI Colors
GREEN = "\033[92m"; YELLOW = "\033[93m"; RED = "\033[91m"; BLUE = "\033[94m"; RESET = "\033[0m"

# --- Configuration ---
APP_NAME = "planner"
APP_MODULE = "Planner" 
COMPANY_NAME = "YOUR COMPANY / NAME"

def log(msg, color=BLUE, logfile=None):
    print(f"{color}{msg}{RESET}")
    if logfile:
        with open(logfile, "a") as f:
            f.write(msg + "\n")

def safe(name: str) -> str:
    """Convert doctype name to folder/file safe name"""
    return name.lower().replace(" ", "_")

def pascal_case(name: str) -> str:
    """Convert doctype name to PascalCase for class names"""
    return name.replace(" ", "").title()

def write_file(path, content, dry_run=False):
    if dry_run:
        return
    with open(path, "w") as f:
        f.write(content)

def scaffold(app_path, config, force=False, dry_run=False, logfile=None):
    app_pkg_dir = os.path.join(app_path, APP_NAME)
    app_doctype_dir = os.path.join(app_pkg_dir, "doctype")
    os.makedirs(app_doctype_dir, exist_ok=True)

    created, skipped = [], []

    # --- NEW: Default Permissions for System Manager ---
    default_permissions = [
        {
            "role": "System Manager",
            "read": 1,
            "write": 1,
            "create": 1,
            "delete": 1,
            "print": 1,
            "email": 1,
            "report": 1,
            "export": 1,
            "share": 1
        }
    ]

    for name in config["order"]:
        safe_name = safe(name)
        folder = os.path.join(app_doctype_dir, safe_name)
        os.makedirs(folder, exist_ok=True)

        init_path = os.path.join(folder, "__init__.py")
        json_path = os.path.join(folder, f"{safe_name}.json")
        py_path   = os.path.join(folder, f"{safe_name}.py")
        js_path   = os.path.join(folder, f"{safe_name}.js")
        test_path = os.path.join(folder, f"test_{safe_name}.py")

        if os.path.exists(json_path) and not force:
            skipped.append(name)
            continue
        
        py_content = f"""# Copyright (c) 2025, {COMPANY_NAME} and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class {pascal_case(name)}(Document):
\tpass
"""

        js_content = f"""// Copyright (c) 2025, {COMPANY_NAME} and contributors
// For license information, please see license.txt

// frappe.ui.form.on("{name}", {{
// \trefresh(frm) {{

// \t}},
// }});
"""

        test_content = f"""# Copyright (c) 2025, {COMPANY_NAME} and Contributors
# See license.txt

# import frappe
from frappe.tests import IntegrationTestCase


class Test{pascal_case(name)}(IntegrationTestCase):
\tpass
"""
        # --- Build DocType JSON Spec ---
        spec = {
            "doctype": "DocType",
            "name": name,
            "module": APP_MODULE,
            "custom": 0,
            "engine": "InnoDB",
            "editable_grid": 1,
            "track_changes": 1,
            "fields": config["doctypes"][name].get("fields", []),
            # --- MODIFIED: Use default_permissions if none are provided ---
            "permissions": config["doctypes"][name].get("permissions", default_permissions),
            "sort_field": "modified",
            "sort_order": "DESC",
            "states": []
        }
        if config["doctypes"][name].get("istable"):
            spec["istable"] = 1
        if config["doctypes"][name].get("autoname"):
            spec["autoname"] = config["doctypes"][name]["autoname"]

        # --- Write all files ---
        write_file(init_path, "", dry_run)
        write_file(json_path, json.dumps(spec, indent=1, sort_keys=True), dry_run)
        write_file(py_path, py_content, dry_run)
        write_file(js_path, js_content, dry_run)
        write_file(test_path, test_content, dry_run)
        
        created.append(name)
        log(f"✅ Scaffolded {name}", GREEN, logfile)

    log("\nSummary:", BLUE, logfile)
    log(f"  Created: {len(created)} -> {created}", GREEN, logfile)
    log(f"  Skipped: {len(skipped)} -> {skipped}", YELLOW, logfile)

def run(force=False, dry_run=False, logfile=None):
    """Entry point for bench execute"""
    app_path = frappe.get_app_path(APP_NAME)
    cfg_path = os.path.join(app_path, "doctypes.json")

    if not os.path.exists(cfg_path):
        log(f"❌ doctypes.json not found in the '{APP_NAME}' app directory.", RED)
        return

    with open(cfg_path) as f:
        config = json.load(f)

    scaffold(app_path, config, force=force, dry_run=dry_run, logfile=logfile)