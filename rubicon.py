import pandas as pd
import os
import re
from datetime import datetime


# ============================================================
# BANKING MANAGEMENT SYSTEM
# ============================================================

MIN_BALANCE = 1000

CUSTOMER_FILE = "customers.csv"
TRANSACTION_FILE = "transactions.csv"
LOAN_FILE = "loans.csv"


# ============================================================
# FILE INITIALIZATION
# ============================================================

def initialize_files():

    if not os.path.exists(CUSTOMER_FILE):

        customers = pd.DataFrame(columns=[
            "account_no",
            "name",
            "age",
            "phone",
            "email",
            "account_type",
            "balance"
        ])

        customers.to_csv(CUSTOMER_FILE, index=False)

    if not os.path.exists(TRANSACTION_FILE):

        transactions = pd.DataFrame(columns=[
            "transaction_id",
            "account_no",
            "transaction_type",
            "amount",
            "date"
        ])

        transactions.to_csv(TRANSACTION_FILE, index=False)

    if not os.path.exists(LOAN_FILE):

        loans = pd.DataFrame(columns=[
            "loan_id",
            "account_no",
            "loan_type",
            "loan_amount",
            "status",
            "date"
        ])

        loans.to_csv(LOAN_FILE, index=False)


# ============================================================
# LOAD DATA
# ============================================================

def load_customers():
    return pd.read_csv(CUSTOMER_FILE)


def load_transactions():
    return pd.read_csv(TRANSACTION_FILE)


def load_loans():
    return pd.read_csv(LOAN_FILE)


# ============================================================
# SAVE DATA
# ============================================================

def save_customers(data):
    data.to_csv(CUSTOMER_FILE, index=False)


def save_transactions(data):
    data.to_csv(TRANSACTION_FILE, index=False)


def save_loans(data):
    data.to_csv(LOAN_FILE, index=False)


# ============================================================
# VALIDATION FUNCTIONS
# ============================================================

def validate_name(name):

    if not name.strip():
        return False

    if not name.replace(" ", "").isalpha():
        return False

    return True


def validate_age(age):

    if not age.isdigit():
        return False

    age = int(age)

    if age < 18 or age > 100:
        return False

    return True


def validate_phone(phone):

    # Indian 10-digit phone number
    pattern = r"^[6-9][0-9]{9}$"

    return re.match(pattern, phone) is not None


def validate_email(email):

    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    return re.match(pattern, email) is not None


def validate_amount(amount):

    try:

        amount = float(amount)

        if amount <= 0:
            return False

        return True

    except ValueError:

        return False


# ============================================================
# GENERATE ACCOUNT NUMBER
# ============================================================

def generate_account_number():

    customers = load_customers()

    if len(customers) == 0:
        return 1001

    return int(customers["account_no"].max()) + 1


# ============================================================
# GENERATE TRANSACTION ID
# ============================================================

def generate_transaction_id():

    transactions = load_transactions()

    return f"T{len(transactions) + 1:04d}"


# ============================================================
# GENERATE LOAN ID
# ============================================================

def generate_loan_id():

    loans = load_loans()

    return f"L{len(loans) + 1:04d}"


# ============================================================
# CREATE ACCOUNT
# ============================================================

def create_account():

    customers = load_customers()

    print("\n===================================")
    print("         CREATE ACCOUNT")
    print("===================================")

    # ---------------- NAME ----------------

    while True:

        name = input("Enter customer name: ").strip()

        if validate_name(name):
            break

        print("Invalid name. Please enter alphabets only.")

    # ---------------- AGE ----------------

    while True:

        age = input("Enter age: ").strip()

        if validate_age(age):
            age = int(age)
            break

        print("Age must be between 18 and 100.")

    # ---------------- PHONE ----------------

    while True:

        phone = input("Enter 10-digit phone number: ").strip()

        if not validate_phone(phone):

            print(
                "Invalid phone number."
                "\nPhone must contain 10 digits "
                "and start with 6, 7, 8 or 9."
            )

            continue

        # Check duplicate phone

        if phone in customers["phone"].astype(str).values:

            print("This phone number is already registered.")

            return

        break

    # ---------------- EMAIL ----------------

    while True:

        email = input("Enter email address: ").strip()

        if not validate_email(email):

            print("Invalid email address.")

            continue

        # Check duplicate email

        if email.lower() in customers["email"].astype(str).str.lower().values:

            print("This email is already registered.")

            return

        break

    # ---------------- ACCOUNT TYPE ----------------

    print("\nAccount Types")

    print("1. Savings")
    print("2. Current")

    while True:

        choice = input("Enter choice: ").strip()

        if choice == "1":

            account_type = "Savings"
            break

        elif choice == "2":

            account_type = "Current"
            break

        else:

            print("Invalid choice.")

    # ---------------- OPENING BALANCE ----------------

    while True:

        balance_input = input(
            f"Enter opening balance (minimum ₹{MIN_BALANCE}): "
        ).strip()

        if not validate_amount(balance_input):

            print("Enter a valid positive amount.")

            continue

        balance = float(balance_input)

        if balance < MIN_BALANCE:

            print(
                f"Opening balance must be at least ₹{MIN_BALANCE}."
            )

            continue

        break

    # ---------------- CREATE ACCOUNT ----------------

    account_no = generate_account_number()

    new_customer = pd.DataFrame([{

        "account_no": account_no,
        "name": name,
        "age": age,
        "phone": phone,
        "email": email,
        "account_type": account_type,
        "balance": balance

    }])

    customers = pd.concat(
        [customers, new_customer],
        ignore_index=True
    )

    save_customers(customers)

    print("\n===================================")
    print("      ACCOUNT CREATED SUCCESSFULLY")
    print("===================================")

    print("Account Number :", account_no)
    print("Customer Name  :", name)
    print("Account Type   :", account_type)
    print("Opening Balance:", balance)


# ============================================================
# VIEW ACCOUNT
# ============================================================

def view_account():

    customers = load_customers()

    print("\n===================================")
    print("           VIEW ACCOUNT")
    print("===================================")

    account_input = input("Enter account number: ").strip()

    if not account_input.isdigit():

        print("Account number must contain digits only.")

        return

    account_no = int(account_input)

    customer = customers[
        customers["account_no"] == account_no
    ]

    if customer.empty:

        print("Account not found.")

        return

    print("\nAccount Details")

    print(customer.to_string(index=False))


# ============================================================
# CREDIT / DEPOSIT
# ============================================================

def credit_money():

    customers = load_customers()

    print("\n===================================")
    print("          CREDIT MONEY")
    print("===================================")

    account_input = input("Enter account number: ").strip()

    if not account_input.isdigit():

        print("Invalid account number.")

        return

    account_no = int(account_input)

    amount_input = input("Enter amount to deposit: ").strip()

    if not validate_amount(amount_input):

        print("Enter a valid positive amount.")

        return

    amount = float(amount_input)

    index = customers.index[
        customers["account_no"] == account_no
    ]

    if len(index) == 0:

        print("Account not found.")

        return

    index = index[0]

    customers.loc[index, "balance"] += amount

    save_customers(customers)

    # Transaction record

    transactions = load_transactions()

    new_transaction = pd.DataFrame([{

        "transaction_id": generate_transaction_id(),
        "account_no": account_no,
        "transaction_type": "Credit",
        "amount": amount,
        "date": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    }])

    transactions = pd.concat(
        [transactions, new_transaction],
        ignore_index=True
    )

    save_transactions(transactions)

    print("\nAmount credited successfully.")

    print(
        "Current Balance:",
        customers.loc[index, "balance"]
    )


# ============================================================
# DEBIT / WITHDRAW
# ============================================================

def debit_money():

    customers = load_customers()

    print("\n===================================")
    print("          DEBIT MONEY")
    print("===================================")

    account_input = input("Enter account number: ").strip()

    if not account_input.isdigit():

        print("Invalid account number.")

        return

    account_no = int(account_input)

    amount_input = input("Enter withdrawal amount: ").strip()

    if not validate_amount(amount_input):

        print("Enter a valid positive amount.")

        return

    amount = float(amount_input)

    index = customers.index[
        customers["account_no"] == account_no
    ]

    if len(index) == 0:

        print("Account not found.")

        return

    index = index[0]

    current_balance = customers.loc[
        index,
        "balance"
    ]

    # Minimum balance constraint

    if current_balance - amount < MIN_BALANCE:

        print(
            f"Transaction denied."
            f"\nMinimum balance of ₹{MIN_BALANCE} "
            f"must be maintained."
        )

        return

    customers.loc[index, "balance"] -= amount

    save_customers(customers)

    # Transaction record

    transactions = load_transactions()

    new_transaction = pd.DataFrame([{

        "transaction_id": generate_transaction_id(),
        "account_no": account_no,
        "transaction_type": "Debit",
        "amount": amount,
        "date": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    }])

    transactions = pd.concat(
        [transactions, new_transaction],
        ignore_index=True
    )

    save_transactions(transactions)

    print("\nWithdrawal successful.")

    print(
        "Remaining Balance:",
        customers.loc[index, "balance"]
    )


# ============================================================
# NET BANKING / FUND TRANSFER
# ============================================================

def fund_transfer():

    customers = load_customers()

    print("\n===================================")
    print("       NET BANKING / TRANSFER")
    print("===================================")

    sender_input = input(
        "Enter sender account number: "
    ).strip()

    receiver_input = input(
        "Enter receiver account number: "
    ).strip()

    if not sender_input.isdigit() or not receiver_input.isdigit():

        print("Account numbers must contain digits only.")

        return

    sender = int(sender_input)
    receiver = int(receiver_input)

    if sender == receiver:

        print("Sender and receiver cannot be the same.")

        return

    amount_input = input(
        "Enter transfer amount: "
    ).strip()

    if not validate_amount(amount_input):

        print("Enter a valid positive amount.")

        return

    amount = float(amount_input)

    sender_index = customers.index[
        customers["account_no"] == sender
    ]

    receiver_index = customers.index[
        customers["account_no"] == receiver
    ]

    if len(sender_index) == 0:

        print("Sender account not found.")

        return

    if len(receiver_index) == 0:

        print("Receiver account not found.")

        return

    sender_index = sender_index[0]
    receiver_index = receiver_index[0]

    sender_balance = customers.loc[
        sender_index,
        "balance"
    ]

    # Minimum balance constraint

    if sender_balance - amount < MIN_BALANCE:

        print(
            f"Transfer denied."
            f"\nSender must maintain minimum "
            f"balance of ₹{MIN_BALANCE}."
        )

        return

    # Debit sender

    customers.loc[
        sender_index,
        "balance"
    ] -= amount

    # Credit receiver

    customers.loc[
        receiver_index,
        "balance"
    ] += amount

    save_customers(customers)

    # Transaction records

    transactions = load_transactions()

    transaction1 = pd.DataFrame([{

        "transaction_id": generate_transaction_id(),
        "account_no": sender,
        "transaction_type": "Transfer Debit",
        "amount": amount,
        "date": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    }])

    transactions = pd.concat(
        [transactions, transaction1],
        ignore_index=True
    )

    transaction2 = pd.DataFrame([{

        "transaction_id": generate_transaction_id(),
        "account_no": receiver,
        "transaction_type": "Transfer Credit",
        "amount": amount,
        "date": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    }])

    transactions = pd.concat(
        [transactions, transaction2],
        ignore_index=True
    )

    save_transactions(transactions)

    print("\nTransfer successful.")


# ============================================================
# TRANSACTION HISTORY
# ============================================================

def transaction_history():

    transactions = load_transactions()

    print("\n===================================")
    print("        TRANSACTION HISTORY")
    print("===================================")

    account_input = input(
        "Enter account number: "
    ).strip()

    if not account_input.isdigit():

        print("Invalid account number.")

        return

    account_no = int(account_input)

    history = transactions[
        transactions["account_no"] == account_no
    ]

    if history.empty:

        print("No transactions found.")

        return

    print(history.to_string(index=False))


# ============================================================
# LOAN SECTION
# ============================================================

def apply_loan():

    customers = load_customers()

    loans = load_loans()

    print("\n===================================")
    print("           LOAN SECTION")
    print("===================================")

    account_input = input(
        "Enter account number: "
    ).strip()

    if not account_input.isdigit():

        print("Invalid account number.")

        return

    account_no = int(account_input)

    customer = customers[
        customers["account_no"] == account_no
    ]

    if customer.empty:

        print("Account not found.")

        return

    print("\nAvailable Loan Types")

    print("1. Home Loan")
    print("2. Car Loan")
    print("3. Education Loan")
    print("4. Personal Loan")

    choice = input("Enter loan type: ").strip()

    loan_limits = {

        "1": ("Home Loan", 5000000),
        "2": ("Car Loan", 2000000),
        "3": ("Education Loan", 1000000),
        "4": ("Personal Loan", 500000)

    }

    if choice not in loan_limits:

        print("Invalid loan type.")

        return

    loan_type, maximum_amount = loan_limits[choice]

    print(
        f"Maximum loan amount: ₹{maximum_amount}"
    )

    amount_input = input(
        "Enter loan amount: "
    ).strip()

    if not validate_amount(amount_input):

        print("Enter a valid positive amount.")

        return

    amount = float(amount_input)

    if amount > maximum_amount:

        print(
            f"Loan amount cannot exceed "
            f"₹{maximum_amount}."
        )

        return

    loan_id = generate_loan_id()

    new_loan = pd.DataFrame([{

        "loan_id": loan_id,
        "account_no": account_no,
        "loan_type": loan_type,
        "loan_amount": amount,
        "status": "Pending",
        "date": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    }])

    loans = pd.concat(
        [loans, new_loan],
        ignore_index=True
    )

    save_loans(loans)

    print("\nLoan application submitted.")

    print("Loan ID:", loan_id)
    print("Loan Type:", loan_type)
    print("Status: Pending")


# ============================================================
# VIEW LOANS
# ============================================================

def view_loans():

    loans = load_loans()

    print("\n===================================")
    print("           LOAN DETAILS")
    print("===================================")

    account_input = input(
        "Enter account number: "
    ).strip()

    if not account_input.isdigit():

        print("Invalid account number.")

        return

    account_no = int(account_input)

    customer_loans = loans[
        loans["account_no"] == account_no
    ]

    if customer_loans.empty:

        print("No loan records found.")

        return

    print(customer_loans.to_string(index=False))


# ============================================================
# CUSTOMER SERVICES
# ============================================================

def customer_service():

    while True:

        print("\n===================================")
        print("        CUSTOMER SERVICES")
        print("===================================")

        print("1. Update Phone Number")
        print("2. Update Email")
        print("3. Transaction History")
        print("4. View Loan Details")
        print("5. Back to Main Menu")

        choice = input("Enter choice: ").strip()

        # -----------------------------------------
        # UPDATE PHONE
        # -----------------------------------------

        if choice == "1":

            customers = load_customers()

            account_input = input(
                "Enter account number: "
            ).strip()

            if not account_input.isdigit():

                print("Invalid account number.")

                continue

            account_no = int(account_input)

            new_phone = input(
                "Enter new phone number: "
            ).strip()

            if not validate_phone(new_phone):

                print("Invalid phone number.")

                continue

            index = customers.index[
                customers["account_no"] == account_no
            ]

            if len(index) == 0:

                print("Account not found.")

                continue

            # Check duplicate phone

            existing_phone = customers[
                customers["phone"].astype(str) == new_phone
            ]

            if not existing_phone.empty:

                print(
                    "This phone number is already registered."
                )

                continue

            customers.loc[
                index[0],
                "phone"
            ] = new_phone

            save_customers(customers)

            print("Phone number updated successfully.")

        # -----------------------------------------
        # UPDATE EMAIL
        # -----------------------------------------

        elif choice == "2":

            customers = load_customers()

            account_input = input(
                "Enter account number: "
            ).strip()

            if not account_input.isdigit():

                print("Invalid account number.")

                continue

            account_no = int(account_input)

            new_email = input(
                "Enter new email address: "
            ).strip()

            if not validate_email(new_email):

                print("Invalid email address.")

                continue

            index = customers.index[
                customers["account_no"] == account_no
            ]

            if len(index) == 0:

                print("Account not found.")

                continue

            existing_email = customers[
                customers["email"].astype(str).str.lower()
                == new_email.lower()
            ]

            if not existing_email.empty:

                print(
                    "This email is already registered."
                )

                continue

            customers.loc[
                index[0],
                "email"
            ] = new_email

            save_customers(customers)

            print("Email updated successfully.")

        # -----------------------------------------
        # TRANSACTION HISTORY
        # -----------------------------------------

        elif choice == "3":

            transaction_history()

        # -----------------------------------------
        # LOAN DETAILS
        # -----------------------------------------

        elif choice == "4":

            view_loans()

        # -----------------------------------------
        # BACK
        # -----------------------------------------

        elif choice == "5":

            break

        else:

            print("Invalid choice.")


# ============================================================
# MAIN MENU
# ============================================================

def main():

    initialize_files()

    while True:

        print("\n")
        print("=" * 55)
        print("             BANKING MANAGEMENT SYSTEM")
        print("=" * 55)

        print("1. Create Account")
        print("2. View Account")
        print("3. Credit / Deposit Money")
        print("4. Debit / Withdraw Money")
        print("5. Net Banking / Fund Transfer")
        print("6. Transaction History")
        print("7. Apply for Loan")
        print("8. View Loan Details")
        print("9. Customer Services")
        print("10. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":

            create_account()

        elif choice == "2":

            view_account()

        elif choice == "3":

            credit_money()

        elif choice == "4":

            debit_money()

        elif choice == "5":

            fund_transfer()

        elif choice == "6":

            transaction_history()

        elif choice == "7":

            apply_loan()

        elif choice == "8":

            view_loans()

        elif choice == "9":

            customer_service()

        elif choice == "10":

            print("\nThank you for using the Banking System.")

            break

        else:

            print("Invalid choice. Please try again.")


# ============================================================
# START PROGRAM
# ============================================================

if __name__ == "__main__":

    main()