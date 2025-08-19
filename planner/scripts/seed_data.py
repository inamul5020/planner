import frappe
from frappe.utils import nowdate

# ANSI Colors
GREEN = "\033[92m"; YELLOW = "\033[93m"; RED = "\033[91m"; BLUE = "\033[94m"; RESET = "\033[0m"

def log(msg, color=BLUE):
    """Prints a colored message to the console."""
    print(f"{color}{msg}{RESET}")

def seed_customer_departments():
    """Creates default Customer Department records."""
    log("Seeding Customer Departments...", BLUE)
    departments = [
        {"department_name": "Head Office"},
        {"department_name": "IT Department"},
        {"department_name": "Sales Department"},
        {"department_name": "Regional Office - Kandy"},
    ]

    for dept in departments:
        # CORRECTED: Check against the specific field 'department_name'
        if not frappe.db.exists("Customer Department", {"department_name": dept["department_name"]}):
            doc = frappe.get_doc({
                "doctype": "Customer Department",
                "department_name": dept["department_name"]
            })
            doc.insert(ignore_permissions=True)
            log(f"  ✅ Created Customer Department: {dept['department_name']}", GREEN)
        else:
            log(f"  ⏩ Skipped Customer Department: {dept['department_name']} (already exists)", YELLOW)

def seed_lak_packages():
    """Creates default Lak Package records."""
    log("Seeding Lak Packages...", BLUE)
    packages = [
        {"package_name": "Basic Plan", "register_fee": 1000, "monthly_fee": 1500},
        {"package_name": "Family Plan", "register_fee": 1000, "monthly_fee": 2500},
        {"package_name": "Pro Plan", "register_fee": 1500, "monthly_fee": 4000},
    ]

    for pkg in packages:
        # CORRECTED: Check against the specific field 'package_name'
        if not frappe.db.exists("Lak Package", {"package_name": pkg["package_name"]}):
            doc = frappe.get_doc({
                "doctype": "Lak Package",
                "package_name": pkg["package_name"],
                "register_fee": pkg["register_fee"],
                "monthly_fee": pkg["monthly_fee"],
            })
            doc.insert(ignore_permissions=True)
            log(f"  ✅ Created Lak Package: {pkg['package_name']}", GREEN)
        else:
            log(f"  ⏩ Skipped Lak Package: {pkg['package_name']} (already exists)", YELLOW)
            
def seed_customers():
    """Creates sample Customer records. Depends on Departments and Packages."""
    log("Seeding Customers...", BLUE)
    customers = [
        {
            "customer_name": "John Doe", "register_date": nowdate(), "phone_number": "0771234567",
            "package_assigned": "Family Plan", "customer_department": "Head Office", "status": "Active"
        },
        {
            "customer_name": "Jane Smith", "register_date": nowdate(), "phone_number": "0719876543",
            "package_assigned": "Pro Plan", "customer_department": "IT Department", "status": "Active"
        },
    ]

    for cust in customers:
        # CORRECTED: Check against the specific field 'customer_name'
        if not frappe.db.exists("Customer", {"customer_name": cust["customer_name"]}):
            # CORRECTED: Check dependencies against the specific field
            if not frappe.db.exists("Lak Package", {"package_name": cust["package_assigned"]}):
                log(f"  ❌ Failed: Lak Package '{cust['package_assigned']}' not found. Skipping customer '{cust['customer_name']}'.", RED)
                continue
            if not frappe.db.exists("Customer Department", {"department_name": cust["customer_department"]}):
                log(f"  ❌ Failed: Customer Department '{cust['customer_department']}' not found. Skipping customer '{cust['customer_name']}'.", RED)
                continue
                
            doc = frappe.get_doc({"doctype": "Customer", **cust})
            doc.insert(ignore_permissions=True)
            log(f"  ✅ Created Customer: {cust['customer_name']}", GREEN)
        else:
            log(f"  ⏩ Skipped Customer: {cust['customer_name']} (already exists)", YELLOW)


def run():
    """Entry point for the `bench execute` command."""
    log("="*40, BLUE)
    log("Starting Data Seeding...", BLUE)
    
    # 1. Masters (No dependencies)
    seed_customer_departments()
    seed_lak_packages()
    
    # ADDED: Commit the master data to the database before proceeding
    frappe.db.commit()
    log("Master data committed.", BLUE)
    
    # 2. Documents with dependencies
    seed_customers()
    
    # Final commit for any remaining changes
    frappe.db.commit()
    log("Data seeding complete!", BLUE)
    log("="*40, BLUE)