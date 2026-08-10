# Payroll Access Management System
# Bitwise Operations and Functions

# ============================================================
# Permission Flags
# ============================================================

VIEW_PAYROLL = 1 << 0
ENTER_PAYROLL = 1 << 1
APPROVE_PAYROLL = 1 << 2
MANAGE_PAYROLL = 1 << 3
GENERATE_REPORTS = 1 << 4

# ============================================================
# Function 1: Validate Employee Name
# ============================================================

def validate_name(name):
    """Validate the employee name."""
    return len(name.strip()) >= 2

# ============================================================
# Function 2: Assign Permissions Based on Role
# ============================================================

def get_role_permissions(role):
    """Return permissions based on the employee's role."""

    if role == "1":
        # Payroll Clerk
        permissions = (
            VIEW_PAYROLL
            | ENTER_PAYROLL
            | GENERATE_REPORTS
        )
        return permissions

    elif role == "2":
        # Payroll Manager
        permissions = (
            VIEW_PAYROLL
            | ENTER_PAYROLL
            | APPROVE_PAYROLL
            | GENERATE_REPORTS
        )
        return permissions

    elif role == "3":
        # Payroll Administrator
        permissions = (
            VIEW_PAYROLL
            | ENTER_PAYROLL
            | APPROVE_PAYROLL
            | MANAGE_PAYROLL
            | GENERATE_REPORTS
        )
        return permissions

    else:
        return 0


# ============================================================
# Function 3: Check a Permission Using AND
# ============================================================

def check_permission(permissions, permission):
    """Check whether an employee has a particular permission."""
    return (permissions & permission) != 0

# ============================================================
# Function 4: Toggle a Permission Using XOR
# ============================================================

def toggle_permission(permissions, permission):
    """Toggle a permission using XOR."""
    return permissions ^ permission

# ============================================================
# Function 5: Display Employee Permissions
# ============================================================

def display_permissions(permissions):
    """Display all permissions assigned to an employee."""

    permission_list = {
        VIEW_PAYROLL: "View Payroll",
        ENTER_PAYROLL: "Enter Payroll",
        APPROVE_PAYROLL: "Approve Payroll",
        MANAGE_PAYROLL: "Manage Payroll",
        GENERATE_REPORTS: "Generate Reports"
    }

    print("\nEmployee Permissions:")

    for permission, name in permission_list.items():

        if check_permission(permissions, permission):
            print(f"- {name}")

# ============================================================
# Main Program
# ============================================================

def main():

    print("======================================")
    print("         MAVUNO SACCO PAYROLL")
    print("       ACCESS MANAGEMENT SYSTEM")
    print("======================================")

    # --------------------------------------------------------
    # Get and validate employee name
    # --------------------------------------------------------

    name = input("\nEnter employee name: ")

    if not validate_name(name):
        print("Invalid name. Please enter at least 2 characters.")
        return

    # --------------------------------------------------------
    # Select employee role
    # --------------------------------------------------------

    print("\nSelect employee role:")
    print("1. Payroll Clerk")
    print("2. Payroll Manager")
    print("3. Payroll Administrator")

    role = input("Enter role number: ")

    # --------------------------------------------------------
    # Get permissions based on selected role
    # --------------------------------------------------------

    permissions = get_role_permissions(role)

    if permissions == 0:
        print("Invalid role selected.")
        return

    # --------------------------------------------------------
    # Display employee information
    # --------------------------------------------------------

    print("\n======================================")
    print("        EMPLOYEE ACCESS DETAILS")
    print("======================================")

    print(f"Employee: {name}")
    print(f"Permission value: {permissions}")
    print(f"Binary representation: {permissions:05b}")

    # --------------------------------------------------------
    # Display all permissions
    # --------------------------------------------------------

    display_permissions(permissions)

    # ========================================================
    # Permission Checks Using AND
    # ========================================================

    print("\n======================================")
    print("          PERMISSION CHECKS")
    print("======================================")

    # Check Approve Payroll permission

    if check_permission(permissions, APPROVE_PAYROLL):
        print("APPROVE PAYROLL: Allowed")
    else:
        print("APPROVE PAYROLL: Not allowed")

    # Check Generate Reports permission

    if check_permission(permissions, GENERATE_REPORTS):
        print("GENERATE REPORTS: Allowed")
    else:
        print("GENERATE REPORTS: Not allowed")

    # ========================================================
    # XOR Demonstration
    # ========================================================

    print("\n======================================")
    print("          XOR DEMONSTRATION")
    print("======================================")

    # Check the original Generate Reports permission

    original_report_access = check_permission(
        permissions,
        GENERATE_REPORTS
    )

    if original_report_access:
        print("Original Generate Reports permission: ENABLED")
    else:
        print("Original Generate Reports permission: DISABLED")

    print("\nApplying XOR to toggle Generate Reports permission...")

    # XOR toggles the Generate Reports bit

    new_permissions = toggle_permission(
        permissions,
        GENERATE_REPORTS
    )

    # Check the permission after XOR

    new_report_access = check_permission(
        new_permissions,
        GENERATE_REPORTS
    )

    if new_report_access:
        print("After XOR: Generate Reports is ENABLED.")
    else:
        print("After XOR: Generate Reports is DISABLED.")

    # ========================================================
    # Bit Shifting Demonstration
    # ========================================================

    print("\n======================================")
    print("       RIGHT SHIFT DEMONSTRATION")
    print("======================================")

    shifted_value = permissions >> 1

    print(f"Original permission value: {permissions}")
    print(f"Original binary value: {permissions:05b}")

    print(f"\nAfter shifting right by 1 bit: {shifted_value}")
    print(f"Shifted binary value: {shifted_value:05b}")

    # ========================================================
    # System Completion
    # ========================================================

    print("\n======================================")
    print("      COMPLETED SUCCESSFULLY")
    print("======================================")


# ============================================================
# Run the Program
# ============================================================

main()