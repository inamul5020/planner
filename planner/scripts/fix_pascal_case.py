import os
import json
import re
import frappe

# ANSI Colors
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"

# --- Configuration ---
APP_NAME = "planner"

def log(msg, color=BLUE):
    """Prints a colored message to the console."""
    print(f"{color}{msg}{RESET}")

def safe(name: str) -> str:
    """Convert doctype name to folder/file safe name"""
    return name.lower().replace(" ", "_")

def pascal_case(name: str) -> str:
    """Convert doctype name to PascalCase for class names"""
    # Handles names like "Staff Cash Submission" -> "StaffCashSubmission"
    return "".join(word.capitalize() for word in name.replace("_", " ").split())

def run():
    """Entry point for the `bench execute` command."""
    log("="*50)
    log(f"🔎 Starting PascalCase check for app: {APP_NAME}...", BLUE)

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
    fixed_files, correct_files, error_files = [], [], []

    # Regex to find the class definition line, e.g., "class MyDoctype(Document):"
    class_pattern = re.compile(r"class\s+([a-zA-Z0-9_]+)\(Document\):")

    for doctype_name in all_doctypes:
        correct_class_name = pascal_case(doctype_name)
        safe_name = safe(doctype_name)
        
        py_path = os.path.join(app_path, APP_NAME, "doctype", safe_name, f"{safe_name}.py")

        if not os.path.exists(py_path):
            continue

        try:
            with open(py_path, 'r') as f:
                content = f.read()
            
            match = class_pattern.search(content)

            if not match:
                log(f"  ⚠️  Could not find class definition in: {doctype_name}. Skipping.", YELLOW)
                error_files.append(doctype_name)
                continue

            current_class_name = match.group(1)

            if current_class_name == correct_class_name:
                log(f"  ✅  Correct: {doctype_name} (Class: {current_class_name})", GREEN)
                correct_files.append(doctype_name)
            else:
                log(f"  🔧 Fixing: {doctype_name} (Incorrect: {current_class_name} -> Correct: {correct_class_name})", YELLOW)
                
                # Replace the incorrect class name with the correct one
                new_content = content.replace(current_class_name, correct_class_name)
                
                with open(py_path, 'w') as f:
                    f.write(new_content)
                
                fixed_files.append(doctype_name)

        except Exception as e:
            log(f"  ❌ Error processing {doctype_name}: {e}", RED)
            error_files.append(doctype_name)

    log("\n🛠️  PascalCase Fix Summary:")
    log(f"  Fixed: {len(fixed_files)}", YELLOW)
    log(f"  Already Correct: {len(correct_files)}", GREEN)
    log(f"  Errors/Skipped: {len(error_files)}", RED)
    if fixed_files:
        log("\nIMPORTANT: Please run 'bench restart' to apply the changes.", BLUE)
    log("="*50)