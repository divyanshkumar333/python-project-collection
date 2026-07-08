import sys
import json
import os
from datetime import datetime

DATA_FILE = "account_data.json"

# Ensure terminal stdout handles Unicode characters (like ₹) on Windows
if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass


class BankAccount:
    """Represents a bank account with transaction history and persistence."""

    def __init__(self, account_holder: str, account_number: str, balance: float = 0.0, transactions: list = None):
        self.account_holder = account_holder
        self.account_number = account_number
        self.balance = balance
        self.transactions = transactions if transactions is not None else []
        if not self.transactions:
            self._log_transaction("Opening", 0.0, "Account created with ₹0.00 balance")

    def _log_transaction(self, tx_type: str, amount: float, description: str):
        """Logs a transaction with datetime and balance state."""
        self.transactions.append({
            "timestamp": datetime.now().isoformat(),
            "type": tx_type,
            "amount": amount,
            "description": description,
            "balance_after": self.balance
        })
        self.save_to_json()

    def save_to_json(self):
        """Persists account state to a JSON file."""
        data = {
            "account_holder": self.account_holder,
            "account_number": self.account_number,
            "balance": self.balance,
            "transactions": self.transactions
        }
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    @classmethod
    def load_from_json(cls):
        """Loads account state from JSON file if it exists."""
        if not os.path.exists(DATA_FILE):
            return None
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            return cls(
                account_holder=data["account_holder"],
                account_number=data["account_number"],
                balance=data["balance"],
                transactions=data["transactions"]
            )
        except (json.JSONDecodeError, KeyError):
            print("Warning: Data file corrupted. Starting with a new session.")
            return None

    def deposit(self, amount: float) -> bool:
        if amount <= 0:
            print("Error: Deposit amount must be greater than zero.")
            return False
        self.balance += amount
        self._log_transaction("Deposit", amount, "Cash Deposit")
        print(f"Successfully deposited ₹{amount:,.2f}.")
        return True

    def withdraw(self, amount: float, category: str = "General") -> bool:
        if amount <= 0:
            print("Error: Withdrawal amount must be greater than zero.")
            return False
        if amount > self.balance:
            print(f"Error: Insufficient balance. Available: ₹{self.balance:,.2f}.")
            return False
        self.balance -= amount
        self._log_transaction("Withdrawal", amount, f"Withdrawal ({category})")
        print(f"Successfully withdrew ₹{amount:,.2f} ({category}).")
        return True

    def transfer(self, amount: float, dest_acc: str, dest_name: str) -> bool:
        if amount <= 0:
            print("Error: Transfer amount must be greater than zero.")
            return False
        if amount > self.balance:
            print(f"Error: Insufficient balance for transfer.")
            return False
        self.balance -= amount
        desc = f"Transfer to {dest_name} (A/C: {dest_acc})"
        self._log_transaction("Transfer", amount, desc)
        print(f"Successfully transferred ₹{amount:,.2f} to {dest_name}.")
        return True

    def display_balance(self):
        """Displays the current balance of the account."""
        print(f"Current Balance: ₹{self.balance:,.2f}")

    def get_summary_metrics(self):
        """Calculates stats for account statement summary."""
        total_dep = sum(t["amount"] for t in self.transactions if t["type"] == "Deposit")
        total_wd = sum(t["amount"] for t in self.transactions if t["type"] == "Withdrawal")
        total_tr = sum(t["amount"] for t in self.transactions if t["type"] == "Transfer")
        return total_dep, total_wd, total_tr

    def display_details(self):
        total_dep, total_wd, total_tr = self.get_summary_metrics()
        print("\n=============================================")
        print("              ACCOUNT DETAILS                ")
        print("=============================================")
        print(f"Account Holder       : {self.account_holder}")
        print(f"Account Number       : {self.account_number}")
        print(f"Current Balance      : ₹{self.balance:,.2f}")
        print(f"Total Deposits       : ₹{total_dep:,.2f}")
        print(f"Total Withdrawals    : ₹{total_wd:,.2f}")
        print(f"Total Transfers      : ₹{total_tr:,.2f}")
        print(f"Total Transactions   : {len(self.transactions)}")
        print("=============================================")

    def display_statement(self, filtered_txs: list = None, header: str = "ACCOUNT STATEMENT"):
        """Displays transactions in tabular format."""
        tx_list = filtered_txs if filtered_txs is not None else self.transactions
        print(f"\n==================================================================================")
        print(f"                                {header:^40}                                  ")
        print(f"==================================================================================")
        print(f"Holder: {self.account_holder} | Account: {self.account_number}")
        print("----------------------------------------------------------------------------------")
        print(f"{'Date & Time':<20} | {'Type':<10} | {'Description':<32} | {'Amount':<12}")
        print("----------------------------------------------------------------------------------")
        for tx in tx_list:
            dt = datetime.fromisoformat(tx["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
            sign = "+" if tx["type"] in ["Deposit", "Opening"] else "-"
            amt_str = f"{sign}₹{tx['amount']:,.2f}"
            print(f"{dt:<20} | {tx['type']:<10} | {tx['description']:<32} | {amt_str:<12}")
        print("----------------------------------------------------------------------------------")
        print(f"Current Balance: ₹{self.balance:,.2f}")
        print("==================================================================================")

    def display_monthly_summary(self):
        """Displays summary metrics grouped by month."""
        monthly_data = {}
        category_spending = {}
        for tx in self.transactions:
            if tx["type"] == "Opening":
                continue
            month_key = datetime.fromisoformat(tx["timestamp"]).strftime("%Y-%m")
            if month_key not in monthly_data:
                monthly_data[month_key] = {"dep": 0.0, "wd": 0.0, "tr": 0.0, "count": 0}
            
            monthly_data[month_key]["count"] += 1
            if tx["type"] == "Deposit":
                monthly_data[month_key]["dep"] += tx["amount"]
            elif tx["type"] == "Withdrawal":
                monthly_data[month_key]["wd"] += tx["amount"]
                if "Withdrawal (" in tx["description"]:
                    cat = tx["description"].split("Withdrawal (")[1].split(")")[0]
                    category_spending[cat] = category_spending.get(cat, 0.0) + tx["amount"]
            elif tx["type"] == "Transfer":
                monthly_data[month_key]["tr"] += tx["amount"]

        if not monthly_data:
            print("\nNo transaction history recorded yet.")
            return

        print("\n=====================================================================")
        print("                          MONTHLY SUMMARY                            ")
        print("=====================================================================")
        print(f"{'Month':<8} | {'Deposited':<13} | {'Withdrawn/Sent':<15} | {'Net Change':<12} | {'Tx Count':<8}")
        print("---------------------------------------------------------------------")
        for month, data in sorted(monthly_data.items(), reverse=True):
            outflow = data["wd"] + data["tr"]
            net_change = data["dep"] - outflow
            sign = "+" if net_change >= 0 else "-"
            net_str = f"{sign}₹{abs(net_change):,.2f}"
            print(f"{month:<8} | ₹{data['dep']:<12,.2f} | ₹{outflow:<14,.2f} | {net_str:<12} | {data['count']:<8}")
        print("=====================================================================")
        
        if category_spending:
            print("\n-------------------------------------")
            print("     WITHDRAWAL BY CATEGORY (ALL)    ")
            print("-------------------------------------")
            for cat, amt in sorted(category_spending.items(), key=lambda x: x[1], reverse=True):
                print(f"{cat:<18}: ₹{amt:,.2f}")
            print("-------------------------------------")

    def search_transactions(self):
        """Allows searching history by transaction type."""
        print("\n--- Search Transactions ---")
        print("1. Deposits\n2. Withdrawals\n3. Transfers\n4. Go Back")
        choice = input("Enter choice (1-4): ").strip()
        type_map = {"1": "Deposit", "2": "Withdrawal", "3": "Transfer"}
        if choice in type_map:
            target_type = type_map[choice]
            filtered = [t for t in self.transactions if t["type"] == target_type]
            self.display_statement(filtered, f"{target_type.upper()} TRANSACTIONS")
        elif choice != "4":
            print("Error: Invalid choice.")

    def export_statement(self, filepath="statement.txt"):
        """Exports the complete statement to a text file."""
        total_dep, total_wd, total_tr = self.get_summary_metrics()
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write("==================================================================================\n")
                f.write("                                PERSONAL BANKING STATEMENT                        \n")
                f.write("==================================================================================\n")
                f.write(f"Account Holder : {self.account_holder}\n")
                f.write(f"Account Number : {self.account_number}\n")
                f.write(f"Current Balance: ₹{self.balance:,.2f}\n")
                f.write(f"Total Deposits : ₹{total_dep:,.2f} | Total Withdrawals: ₹{total_wd:,.2f} | Total Transfers: ₹{total_tr:,.2f}\n")
                f.write(f"Total Transactions: {len(self.transactions)}\n")
                f.write("----------------------------------------------------------------------------------\n")
                f.write(f"{'Date & Time':<20} | {'Type':<10} | {'Description':<32} | {'Amount':<12}\n")
                f.write("----------------------------------------------------------------------------------\n")
                for tx in self.transactions:
                    dt = datetime.fromisoformat(tx["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
                    sign = "+" if tx["type"] in ["Deposit", "Opening"] else "-"
                    amt_str = f"{sign}₹{tx['amount']:,.2f}"
                    f.write(f"{dt:<20} | {tx['type']:<10} | {tx['description']:<32} | {amt_str:<12}\n")
                f.write("==================================================================================\n")
            print(f"Statement exported successfully to {filepath}")
        except IOError:
            print("Error: Unable to export statement.")


def get_positive_float(prompt: str) -> float:
    while True:
        try:
            val = input(prompt).strip().replace("₹", "").replace(",", "")
            amount = float(val)
            if amount <= 0:
                print("Error: Amount must be greater than zero.")
                continue
            return amount
        except ValueError:
            print("Error: Invalid numeric input.")


def get_validated_input(prompt: str, validator, error_msg: str) -> str:
    while True:
        val = input(prompt).strip()
        if validator(val):
            return val
        print(f"Error: {error_msg}")


def main():
    account = BankAccount.load_from_json()
    if account:
        print(f"\nWelcome back, {account.account_holder}! Account loaded from database.")
    else:
        print("=====================================")
        print("    Welcome to Python Online Bank    ")
        print("=====================================")
        name_val = lambda n: len(n) >= 2 and all(x.isalpha() or x.isspace() for x in n)
        acc_val = lambda a: a.isdigit() and 1 <= len(a) <= 18
        
        holder_name = get_validated_input("Enter Account Holder's Name: ", name_val, "Name must be alphabetical and at least 2 characters.")
        account_num = get_validated_input("Enter Account Number (1-18 digits): ", acc_val, "Account number must be 1-18 numeric digits.")
        account = BankAccount(holder_name, account_num)
        print("\nAccount successfully created!")

    while True:
        print("\n=====================================")
        print("      PERSONAL BANKING SIMULATOR     ")
        print("=====================================")
        print("1. Deposit\n2. Withdraw\n3. Transfer Money\n4. View Balance\n5. Account Details")
        print("6. Transaction History\n7. Monthly Summary\n8. Export Statement\n9. Exit")
        print("=====================================")
        
        choice = input("Enter option (1-9): ").strip()
        if choice == "1":
            amount = get_positive_float("Enter amount to deposit: ₹")
            account.deposit(amount)
        elif choice == "2":
            amount = get_positive_float("Enter amount to withdraw: ₹")
            print("Select Category:\n1. Food\n2. Utilities\n3. Bills\n4. Entertainment\n5. Other")
            cat_choice = input("Enter choice (1-5, default 5): ").strip()
            cat_map = {"1": "Food", "2": "Utilities", "3": "Bills", "4": "Entertainment"}
            category = cat_map.get(cat_choice, "Other")
            account.withdraw(amount, category)
        elif choice == "3":
            dest_name = get_validated_input("Enter Recipient Name: ", lambda n: len(n) >= 2, "Invalid name.")
            dest_acc = get_validated_input("Enter Recipient Account Number: ", lambda a: a.isalnum(), "Invalid account number.")
            amount = get_positive_float("Enter amount to transfer: ₹")
            account.transfer(amount, dest_acc, dest_name)
        elif choice == "4":
            account.display_balance()
        elif choice == "5":
            account.display_details()
        elif choice == "6":
            print("\n1. View All Transactions\n2. Search/Filter Transactions")
            sub_choice = input("Enter option (1-2): ").strip()
            if sub_choice == "1":
                account.display_statement()
            elif sub_choice == "2":
                account.search_transactions()
            else:
                print("Error: Invalid choice.")
        elif choice == "7":
            account.display_monthly_summary()
        elif choice == "8":
            account.export_statement()
        elif choice == "9":
            account.save_to_json()
            print("\nData saved. Thank you for banking with us!")
            break
        else:
            print("Error: Invalid option. Select between 1 and 9.")


if __name__ == "__main__":
    main()
