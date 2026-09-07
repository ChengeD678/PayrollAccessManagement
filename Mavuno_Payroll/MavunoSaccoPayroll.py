# Import modules used for JSON storage, package installation, and system control.
import json
import importlib.util
import subprocess
import sys

# Define bitwise permission values. Each permission uses a different binary bit.
VIEW_PAYROLL = 1
EDIT_PAYROLL = 2
MANAGE_EMPLOYEES = 4

#Checks if colorama and tabulate are installed, if not installs them. If installation fails, exits the program.
def ensure_package(package_name, import_name=None):
    if import_name is None:
        import_name = package_name

    if importlib.util.find_spec(import_name) is not None:
        print(f"{package_name} is already installed.")
        return True

    print(f"{package_name} is not installed. Installing...")

    try:
        subprocess.check_call([
            sys.executable,
            "-m",
            "pip",
            "install",
            package_name
        ])

        print(f"{package_name} installed successfully.")
        return True

    except subprocess.CalledProcessError:
        print(f"Failed to install {package_name}.")
        return False
    
if not ensure_package("colorama"):
    sys.exit()

if not ensure_package("tabulate"):
    sys.exit()

# Import the external libraries used for terminal colours and formatted tables.
from colorama import init, Fore
from tabulate import tabulate

init(autoreset=True)

def has_permission(permissions, permission):
    return (permissions & permission) != 0

# Calculate Paye. Starts with zero tax.
def calculate_paye(taxable_income):
    tax = 0
    remaining = taxable_income

    # First KSh 24,000 at 10%
    if remaining > 0:
        amount = min(remaining, 24000)
        tax += amount * 0.10
        remaining -= amount

    # Next KSh 8,333 at 25%
    if remaining > 0:
        amount = min(remaining, 8333)
        tax += amount * 0.25
        remaining -= amount

    # Next KSh 467,667 at 30%
    if remaining > 0:
        amount = min(remaining, 467667)
        tax += amount * 0.30
        remaining -= amount

    # Next KSh 300,000 at 32.5%
    if remaining > 0:
        amount = min(remaining, 300000)
        tax += amount * 0.325
        remaining -= amount

    # Anything above KSh 800,000 at 35%
    if remaining > 0:
        tax += remaining * 0.35

    # Personal relief
    tax -= 2400

    if tax < 0:
        tax = 0

    return tax

# Calculate nssf limitting the pensionable salary to the configured NSSF ceiling.
def calculate_nssf(gross_salary):
    pensionable_salary = min(gross_salary, 108000)
    nssf = pensionable_salary * 0.06
    return nssf

# Calculate shif based on the configured SHIF rate of 2.75% of gross salary.
def calculate_shif(gross_salary):
    shif = gross_salary * 0.0275
    return shif

#calculate affordable housing levy based on the configured AHL rate of 1.5% of gross salary.
def calculate_ahl(gross_salary):
    ahl = gross_salary * 0.015
    return ahl


def calculate_gross_salary(basic_salary, allowances):
    gross_salary = basic_salary + allowances
    return gross_salary

# Display in currency formart with Ksh prefix
def format_currency(amount):
    return f"KSh {amount:,.2f}"

def calculate_payroll(employee):
    gross_salary = calculate_gross_salary(
        employee["basic_salary"],
        employee["allowances"]
    )

    nssf = calculate_nssf(gross_salary)
    shif = calculate_shif(gross_salary)
    ahl = calculate_ahl(gross_salary)

    taxable_income = gross_salary - nssf - shif - ahl

    paye = calculate_paye(taxable_income)

    total_deductions = paye + nssf + shif + ahl

    net_salary = gross_salary - total_deductions

    return gross_salary, paye, nssf, shif, ahl, total_deductions, net_salary

def payroll_summary(employees):
    total_gross = 0
    total_paye = 0
    total_nssf = 0
    total_shif = 0
    total_ahl = 0
    total_net = 0

    for employee in employees:
        (
            gross_salary,
            paye,
            nssf,
            shif,
            ahl,
            total_deductions,
            net_salary
        ) = calculate_payroll(employee)

        total_gross += gross_salary
        total_paye += paye
        total_nssf += nssf
        total_shif += shif
        total_ahl += ahl
        total_net += net_salary

    return (
        total_gross,
        total_paye,
        total_nssf,
        total_shif,
        total_ahl,
        total_net
    )

def display_menu():
    print("\n" + "MAVUNO SACCO PAYROLL SYSTEM".center(40))
    print("=" * 40)
    print("1. Display Employees")
    print("2. Add Employee")
    print("3. Search Employee")
    print("4. Generate Payslip")
    print("5. Check Employee Permissions")
    print("6. Assign Permission")
    print("7. Payroll Summary")
    print("8. Exit")

def add_employee(employees):
    employee_id = input("Enter employee ID: ")
    
    for employee in employees:
        if employee["id"] == employee_id:
            print(Fore.RED + "Employee ID already exists.")
            return
        
    name = input("Enter employee name: ")
    department = input("Enter department: ")

    while True:
        try:
            # Get and validate the basic salary.
            basic_salary = float(input("Enter basic salary: "))

            if basic_salary < 0:
                print(Fore.RED + "Basic salary cannot be negative.")
                continue

             # Get and validate the allowances.
            allowances = float(input("Enter allowances: "))

            if allowances < 0:
                print(Fore.RED + "Allowances cannot be negative.")
                continue

            break

        except ValueError:
            # Handle input that cannot be converted to a number.
            print(Fore.RED + "Invalid salary. Please enter numbers only.")

    # Store the new employee as a dictionary so it can be added to the employee list.
    employee = {
        "id": employee_id,
        "name": name,
        "department": department,
        "basic_salary": basic_salary,
        "allowances": allowances
    }

    employees.append(employee)
    save_employees(employees)

    print(Fore.GREEN + "Employee added successfully.")
    
def search_employee(employees):
    search_id = input("Enter employee ID to search: ")

    # Process each employee in the list one at a time.
    for employee in employees:
        if employee["id"] == search_id:
            print("Employee found:")

            table = [[
                employee["id"],
                employee["name"],
                employee["department"],
                employee["basic_salary"],
                employee["allowances"]
]]

            print(tabulate(
                table,
                headers=[
                    "ID",
                    "Name",
                    "Department",
                    "Basic Salary",
                    "Allowances"
            
                ],
                tablefmt="grid"
            ))

            return

    print("Employee not found.")
    
def generate_payslip(employees):
    employee_id = input("Enter employee ID: ")

    for employee in employees:
        if employee["id"] == employee_id:

            (
                gross_salary,
                paye,
                nssf,
                shif,
                ahl,
                total_deductions,
                net_salary
            ) = calculate_payroll(employee)

            print("\nPAYSLIP")
            print("=" * 40)
            print("Employee ID:", employee["id"])
            print("Name:", employee["name"])
            print("Department:", employee["department"])
            print("-" * 40)
            print("Basic Salary:", format_currency(employee["basic_salary"]))
            print("Allowances:", format_currency(employee["allowances"]))
            print("Gross Salary:", format_currency(gross_salary))
            print("-" * 40)
            print("PAYE:", format_currency(paye))
            print("NSSF:", format_currency(nssf))
            print("SHIF:", format_currency(shif))
            print("AHL:", format_currency(ahl))
            print("Net Salary:", format_currency(net_salary))
            print("=" * 40)

            return

    print("Employee not found.")
    
def check_employee_permission(employees):
    employee_id = input("Enter employee ID: ")

    for employee in employees:
        if employee["id"] == employee_id:
            permissions = employee.get("permissions", 0)

            print("Employee:", employee["name"])

            if has_permission(permissions, VIEW_PAYROLL):
                print("- Can view payroll: Yes")
            else:
                print("- Can view payroll: No")

            if has_permission(permissions, EDIT_PAYROLL):
                print("- Can edit payroll: Yes")
            else:
                print("- Can edit payroll: No")

            if has_permission(permissions, MANAGE_EMPLOYEES):
                print("- Can manage employees: Yes")
            else:
                print("- Can manage employees: No")

            return

    print("Employee not found.")
    
def assign_permissions(employees):
    employee_id = input("Enter employee ID: ")

    for employee in employees:
        if employee["id"] == employee_id:

            print("1. View Payroll")
            print("2. Edit Payroll")
            print("3. Manage Employees")

            choice = input("Select permission: ")

            if choice == "1":
                employee["permissions"] = employee.get("permissions", 0) | VIEW_PAYROLL

            elif choice == "2":
                employee["permissions"] = employee.get("permissions", 0) | EDIT_PAYROLL

            elif choice == "3":
                employee["permissions"] = employee.get("permissions", 0) | MANAGE_EMPLOYEES

            else:
                print(Fore.RED + "Invalid permission.")
                return

            save_employees(employees)
            print(Fore.GREEN + "Permission assigned successfully.")
            return

    print("Employee not found.")

def save_employees(employees):
    try:
        with open("employees.json", "w") as file:
            json.dump(employees, file, indent=4)

        print("Employee records saved successfully.")

    except IOError:
        print("Error saving employee records.")
        
def load_employees():
    try:
        with open("employees.json", "r") as file:
            employees = json.load(file)

        return employees

    except FileNotFoundError:
        return []

# Initial sample employee records.
employees = [
    {
        "id": "EMP001",
        "name": "Amina Wanjiku",
        "department": "Finance",
        "basic_salary": 85000,
        "allowances": 10000
    },

    {
        "id": "EMP002",
        "name": "Brian Otieno",
        "department": "IT",
        "basic_salary": 120000,
        "allowances": 15000
    },

    {
        "id": "EMP003",
        "name": "Carol Njeri",
        "department": "HR",
        "basic_salary": 55000,
        "allowances": 5000,
        "permissions": VIEW_PAYROLL | EDIT_PAYROLL
    },

    {
        "id": "EMP004",
        "name": "Davis Chenge",
        "department": "Credit",
        "basic_salary": 180000,
        "allowances": 16000
    },

    {
        "id": "EMP005",
        "name": "Andrew Shisia",
        "department": "Intern",
        "basic_salary": 18000,
        "allowances": 0
    }
]

# Load the actual employee records from employees.json for persistent storage. New employees added will be saved to the Json file.
employees = load_employees()

# Keep the application running until the user selects the Exit option.
while True:
    display_menu()

    choice = input("Enter your choice: ")

    if choice == "1":
        # Create a list that will hold the rows displayed by Tabulate.
        table = []

        for employee in employees:
            (
                gross_salary,
                paye,
                nssf,
                shif,
                ahl,
                total_deductions,
                net_salary
            ) = calculate_payroll(employee)

            # Add the current employee's calculated payroll values as one table row.
            table.append([
                employee["id"],
                employee["name"],
                employee["department"],
                format_currency(gross_salary),
                format_currency(paye),
                format_currency(nssf),
                format_currency(shif),
                format_currency(ahl),
                format_currency(net_salary)

            ])
        print(tabulate(
            table,
            headers=[
                "ID",
                "Name",
                "Department",
                "Gross",
                "PAYE",
                "NSSF",
                "SHIF",
                "AHL",
                "Net"
            ],
            tablefmt="grid"
        ))

    elif choice == "2":
        add_employee(employees)
        
    elif choice == "3":
        search_employee(employees)
        
    elif choice == "4":
        generate_payslip(employees)
        
    elif choice == "5":
        check_employee_permission(employees)
        
    elif choice == "6":
        assign_permissions(employees)
        
    elif choice == "7":
        (
            total_gross,
            total_paye,
            total_nssf,
            total_shif,
            total_ahl,
            total_net
        ) = payroll_summary(employees)

        print("\nPAYROLL SUMMARY")
        print("================")
        print("Total Gross:", format_currency(total_gross))
        print("Total PAYE:", format_currency(total_paye))
        print("Total NSSF:", format_currency(total_nssf))
        print("Total SHIF:", format_currency(total_shif))
        print("Total AHL:", format_currency(total_ahl))
        print("Total Net Payroll:", format_currency(total_net))

    elif choice == "8":
        print("Exiting payroll application...")
        break
    
    
    else:
        print(Fore.RED + "Invalid choice. Please try again.")