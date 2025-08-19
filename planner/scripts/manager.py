import frappe
import os

# Import the main 'run' function from each of our stable scripts
from .scaffold_doctypes import run as scaffold
from .fix_pascal_case import run as fix_pascal_case
from .load_doctypes import run as load
from .seed_data import run as seed
from .verify_doctypes import run as verify_doctypes
from .verify_data import run as verify_data

# ANSI Colors for logging
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

def log(msg, color=BLUE):
    """Prints a colored message to the console."""
    print(f"{color}--- {msg} ---{RESET}")

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def run():
    """
    Presents an interactive menu to run various setup and verification scripts.
    """
    while True:
        clear_screen()
        print(f"{BLUE}========================================={RESET}")
        print(f"{BLUE}      Frappe App Manager for 'planner'     {RESET}")
        print(f"{BLUE}========================================={RESET}")
        print(f"{GREEN}1. Scaffold DocTypes{RESET}")
        print(f"{GREEN}2. Load DocTypes (includes PascalCase fix){RESET}")
        print(f"{GREEN}3. Seed Data{RESET}")
        print(f"{YELLOW}-----------------------------------------{RESET}")
        print(f"{GREEN}4. Run Full Setup (Scaffold -> Load -> Seed){RESET}")
        print(f"{YELLOW}-----------------------------------------{RESET}")
        print(f"{GREEN}5. Fix PascalCase in Controllers{RESET}")
        print(f"{GREEN}6. Verify DocTypes Exist{RESET}")
        print(f"{GREEN}7. Verify Seed Data Exists{RESET}")
        print(f"{YELLOW}-----------------------------------------{RESET}")
        print(f"{GREEN}0. Exit{RESET}")
        print(f"{BLUE}========================================={RESET}")

        choice = input("Enter your choice: ")

        if choice == '1':
            log("Action: Scaffold DocTypes")
            force_input = input("Force overwrite existing files? (y/n): ").lower()
            force = force_input == 'y'
            scaffold(force=force)
            
        elif choice == '2':
            log("Action: Load DocTypes")
            log("Running PascalCase check before loading...")
            fix_pascal_case()
            log("Proceeding with loading DocTypes...")
            load()

        elif choice == '3':
            log("Action: Seed Data")
            seed()

        elif choice == '4':
            log("Action: Run Full Setup")
            force_input = input("Force overwrite existing files during scaffold? (y/n): ").lower()
            force = force_input == 'y'
            scaffold(force=force)
            
            log("Running PascalCase check before loading...")
            fix_pascal_case()
            log("Proceeding with loading DocTypes...")
            load()
            
            seed()

        elif choice == '5':
            log("Action: Fix PascalCase")
            fix_pascal_case()

        elif choice == '6':
            log("Action: Verify DocTypes")
            verify_doctypes()

        elif choice == '7':
            log("Action: Verify Seed Data")
            verify_data()

        elif choice == '0':
            log("Exiting Manager.")
            break
            
        else:
            print(f"\n{YELLOW}Invalid choice. Please try again.{RESET}")

        input("\nPress Enter to continue...")