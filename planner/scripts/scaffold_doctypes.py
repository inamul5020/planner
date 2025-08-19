import os
import json
import frappe

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
    return "".join(word.capitalize() for word in name.replace("_", " ").split())

def write_file(path, content, dry_run=False):
    if dry_run: return
    with open(path, "w") as f:
        f.write(content)

def run(force=False, dry_run=False, logfile=None):
    """Entry point for the `bench execute` command."""
    try:
        app_path = frappe.get_app_path(APP_NAME)
        cfg_path = os.path.join(app_path, "doctypes.json")
    except frappe.exceptions.DoesNotExistError:
        log(f"❌ App '{APP_NAME}' not found.", RED); return

    if not os.path.exists(cfg_path):
        log(f"❌ doctypes.json not found.", RED); return

    with open(cfg_path) as f:
        config = json.load(f)

    app_doctype_dir = os.path.join(app_path, APP_NAME, "doctype")
    os.makedirs(app_doctype_dir, exist_ok=True)

    created, updated, skipped = {"json": [], "py": [], "js": [], "test": []}, [], []

    default_permissions = [{"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1, "print": 1, "email": 1, "report": 1, "export": 1, "share": 1}]

    for name in config["order"]:
        log(f"--- Processing: {name} ---", BLUE)
        safe_name = safe(name)
        folder = os.path.join(app_doctype_dir, safe_name)
        os.makedirs(folder, exist_ok=True)

        # Define all paths and content templates
        paths = {
            "json": os.path.join(folder, f"{safe_name}.json"),
            "py": os.path.join(folder, f"{safe_name}.py"),
            "js": os.path.join(folder, f"{safe_name}.js"),
            "test": os.path.join(folder, f"test_{safe_name}.py"),
            "init": os.path.join(folder, "__init__.py"),
        }
        contents = {
            "py": f"""# Copyright (c) 2025, {COMPANY_NAME} and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class {pascal_case(name)}(Document):
\tpass
""",
            "js": f"""// Copyright (c) 2025, {COMPANY_NAME} and contributors
// For license information, please see license.txt

// frappe.ui.form.on("{name}", {{
// \trefresh(frm) {{

// \t}},
// }});
""",
            "test": f"""# Copyright (c) 2025, {COMPANY_NAME} and Contributors
# See license.txt

# import frappe
from frappe.tests import IntegrationTestCase


class Test{pascal_case(name)}(IntegrationTestCase):
\tpass
""",
            "init": ""
        }

        # 1. Handle the JSON file (Create or Update)
        doctype_config = config["doctypes"].get(name, {})
        if not os.path.exists(paths["json"]) or force:
            spec = {
                "doctype": "DocType", "name": name, "module": APP_MODULE, "custom": 0,
                "engine": "InnoDB", "editable_grid": 1, "track_changes": 1,
                "fields": doctype_config.get("fields", []),
                "permissions": doctype_config.get("permissions", default_permissions),
                "autoname": doctype_config.get("autoname"),
                "sort_field": "modified", "sort_order": "DESC", "states": []
            }
            if doctype_config.get("istable"): spec["istable"] = 1
            write_file(paths["json"], json.dumps(spec, indent=1, sort_keys=True), dry_run)
            created["json"].append(name)
            log(f"  ✅ Created {safe_name}.json", GREEN)
        else:
            with open(paths["json"], 'r+') as f:
                existing_spec = json.load(f)
                if not existing_spec.get("permissions"):
                    existing_spec["permissions"] = default_permissions
                    f.seek(0)
                    f.truncate()
                    json.dump(existing_spec, f, indent=1, sort_keys=True)
                    updated.append(name)
                    log(f"  🔄 Updated permissions in {safe_name}.json", YELLOW)

        # 2. Handle the supporting files (py, js, test, init)
        # Create them if they are missing OR empty
        for file_type in ["py", "js", "test", "init"]:
            path = paths[file_type]
            if not os.path.exists(path) or os.path.getsize(path) == 0:
                write_file(path, contents[file_type], dry_run)
                created[file_type].append(name)
                log(f"  ✅ Created {os.path.basename(path)}", GREEN)

    log("\n--- Summary ---", BLUE)
    log(f"JSON Files Created: {len(created['json'])}", GREEN)
    log(f"Python Files Created: {len(created['py'])}", GREEN)
    log(f"JS Files Created: {len(created['js'])}", GREEN)
    log(f"Permissions Updated: {len(updated)}", YELLOW)