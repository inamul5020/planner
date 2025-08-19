import frappe

# ANSI Colors
GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"

def log(msg, color=BLUE):
    """Prints a colored message to the console."""
    print(f"{color}{msg}{RESET}")

def verify_customer_departments():
    """Verifies the existence of default Customer Department records."""
    log("Verifying Customer Departments...", BLUE)
    departments = [
        {"department_name": "Head Office"},
        {"department_name": "IT Department"},
        {"department_name": "Sales Department"},
        {"department_name": "Regional Office - Kandy"},
    ]
    
    found, not_found = 0, 0
    for dept in departments:
        if frappe.db.exists("Customer Department", {"department_name": dept["department_name"]}):
            log(f"  ✅ Found: {dept['department_name']}", GREEN)
            found += 1
        else:
            log(f"  ❌ Not Found: {dept['department_name']}", RED)
            not_found += 1
    return found, not_found

def verify_lak_packages():
    """Verifies the existence of default Lak Package records."""
    log("Verifying Lak Packages...", BLUE)
    packages = [
        {"package_name": "Basic Plan"},
        {"package_name": "Family Plan"},
        {"package_name": "Pro Plan"},
    ]
    
    found, not_found = 0, 0
    for pkg in packages:
        if frappe.db.exists("Lak Package", {"package_name": pkg["package_name"]}):
            log(f"  ✅ Found: {pkg['package_name']}", GREEN)
            found += 1
        else:
            log(f"  ❌ Not Found: {pkg['package_name']}", RED)
            not_found += 1
    return found, not_found
            
def verify_customers():
    """Verifies the existence of sample Customer records."""
    log("Verifying Customers...", BLUE)
    customers = [
        {"customer_name": "John Doe"},
        {"customer_name": "Jane Smith"},
    ]

    found, not_found = 0, 0
    for cust in customers:
        if frappe.db.exists("Customer", {"customer_name": cust["customer_name"]}):
            log(f"  ✅ Found: {cust['customer_name']}", GREEN)
            found += 1
        else:
            log(f"  ❌ Not Found: {cust['customer_name']}", RED)
            not_found += 1
    return found, not_found

def run():
    """Entry point for the `bench execute` command."""
    total_found, total_not_found = 0, 0

    log("="*40, BLUE)
    log("Starting Data Verification...", BLUE)
    
    results = [
        verify_customer_departments(),
        verify_lak_packages(),
        verify_customers(),
    ]
    
    for found, not_found in results:
        total_found += found
        total_not_found += not_found

    log("\n--- Verification Summary ---", BLUE)
    log(f"  Records Found: {total_found}", GREEN)
    log(f"  Records Not Found: {total_not_found}", RED)
    if total_not_found > 0:
        log("\n  Suggestion: Run the seed script to create the missing records.", BLUE)
        log("  `bench --site [your_site_name] execute planner.scripts.seed_data.run`", BLUE)
    log("="*40, BLUE)