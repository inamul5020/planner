import os
import json

APP_NAME = "planner"
MODULE_NAME = "Planner"

# Path where doctypes should live: apps/planner/planner/planner/doctype/
BASE_PATH = os.path.join(
    os.path.dirname(__file__),
    "..", "..", APP_NAME, APP_NAME, "doctype"
)

DOCTYPES_JSON_PATH = os.path.join(
    os.path.dirname(__file__),
    "..", "..", APP_NAME, APP_NAME, "doctypes.json"
)


def make_empty_init(path):
    """Create __init__.py file (empty)."""
    with open(path, "w") as f:
        f.write("")


def make_json(path, doctype_name, fields):
    """Create {doctype}.json file in Frappe’s format."""
    content = {
        "actions": [],
        "allow_rename": 1,
        "creation": "",
        "doctype": "DocType",
        "engine": "InnoDB",
        "field_order": [f["fieldname"] for f in fields] if fields else [],
        "fields": fields if fields else [{
            "fieldname": "title",
            "fieldtype": "Data",
            "label": "Title",
            "reqd": 1,
            "in_list_view": 1
        }],
        "grid_page_length": 50,
        "index_web_pages_for_search": 1,
        "links": [],
        "modified": "",
        "modified_by": "",
        "module": MODULE_NAME,
        "name": doctype_name,
        "owner": "Administrator",
        "permissions": [
            {
                "create": 1,
                "delete": 1,
                "email": 1,
                "export": 1,
                "print": 1,
                "read": 1,
                "report": 1,
                "role": "System Manager",
                "share": 1,
                "write": 1
            }
        ],
        "row_format": "Dynamic",
        "sort_field": "creation",
        "sort_order": "DESC",
        "states": []
    }

    with open(path, "w") as f:
        json.dump(content, f, indent=1)


def make_py(path, doctype_name):
    """Create {doctype}.py controller file."""
    class_name = doctype_name.replace(" ", "")
    content = f'''# Copyright (c) 2025, {APP_NAME} and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class {class_name}(Document):
\tpass
'''
    with open(path, "w") as f:
        f.write(content)


def make_js(path, doctype_name):
    """Create {doctype}.js client script file."""
    content = f'''// Copyright (c) 2025, {APP_NAME}
// For license information, please see license.txt

frappe.ui.form.on('{doctype_name}', {{
\t// refresh: function(frm) {{
\t// }}
}});
'''
    with open(path, "w") as f:
        f.write(content)


def make_test(path, doctype_name):
    """Create test_{doctype}.py unit test file."""
    class_name = doctype_name.replace(" ", "")
    content = f'''# Copyright (c) 2025, {APP_NAME} and contributors
# See license.txt

import frappe
import unittest

class Test{class_name}(unittest.TestCase):
\tpass
'''
    with open(path, "w") as f:
        f.write(content)


def scaffold_doctype(doctype_name, fields):
    """Generate folder + 5 files for a doctype."""
    folder = os.path.join(BASE_PATH, doctype_name.lower().replace(" ", "_"))
    os.makedirs(folder, exist_ok=True)

    make_empty_init(os.path.join(folder, "__init__.py"))
    make_json(os.path.join(folder, f"{doctype_name.lower().replace(' ', '_')}.json"), doctype_name, fields)
    make_py(os.path.join(folder, f"{doctype_name.lower().replace(' ', '_')}.py"), doctype_name)
    make_js(os.path.join(folder, f"{doctype_name.lower().replace(' ', '_')}.js"), doctype_name)
    make_test(os.path.join(folder, f"test_{doctype_name.lower().replace(' ', '_')}.py"), doctype_name)

    print(f"✔ Scaffolded {doctype_name}")


def main():
    with open(DOCTYPES_JSON_PATH) as f:
        doctypes = json.load(f)

    for doctype_name, meta in doctypes.items():
        scaffold_doctype(doctype_name, meta.get("fields", []))


if __name__ == "__main__":
    main()
