import os, json, frappe
from frappe.model.sync import sync_for

# ANSI Colors
GREEN = "\033[92m"; YELLOW = "\033[93m"; RED = "\033[91m"; BLUE = "\033[94m"; RESET = "\033[0m"

# --- Configuration ---
# Updated to match your app name
APP_NAME = "planner"
APP_MODULE = "Planner"

def log(msg, color=BLUE, logfile=None):
    """Prints a colored message to the console."""
    print(f"{color}{msg}{RESET}")
    if logfile:
        with open(logfile, "a") as f:
            f.write(msg + "\n")

def safe(name: str) -> str:
    """Converts DocType name to a file-safe name."""
    return name.lower().replace(" ", "_")

def load_all(config, logfile=None):
    """Loops through doctypes.json and syncs each one to the database."""
    synced, skipped = [], []

    log(f"Starting DocType sync for app: {APP_NAME}...", BLUE, logfile)
    for name in config["order"]:
        log(f"🔄 Syncing '{name}'...", BLUE, logfile)
        try:
            # This is the core Frappe function that syncs a doctype
            # from the app's JSON file to the database schema.
            sync_for(APP_NAME, safe(name))
            synced.append(name)
            log(f"✅ Synced '{name}' successfully.", GREEN, logfile)
        except Exception as e:
            skipped.append(name)
            log(f"❌ Failed to sync '{name}': {e}", RED, logfile)

    log("\n" + "="*40, BLUE, logfile)
    log("Sync Summary:", BLUE, logfile)
    log(f"  Synced: {len(synced)} -> {synced}", GREEN, logfile)
    log(f"  Skipped: {len(skipped)} -> {skipped}", YELLOW, logfile)
    log("="*40, BLUE, logfile)


def run(logfile=None):
    """Entry point for the `bench execute` command."""
    try:
        app_path = frappe.get_app_path(APP_NAME)
        cfg_path = os.path.join(app_path, "doctypes.json")
    except frappe.exceptions.DoesNotExistError:
        log(f"❌ App '{APP_NAME}' not found. Please check the APP_NAME variable in the script.", RED)
        return


    if not os.path.exists(cfg_path):
        log(f"❌ doctypes.json not found in the '{APP_NAME}' app directory.", RED, logfile)
        return

    with open(cfg_path) as f:
        config = json.load(f)

    load_all(config, logfile=logfile)