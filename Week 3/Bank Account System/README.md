# Personal Banking Simulator

An interactive command-line banking simulator written in Python 3. this application demonstrates OOP design, data persistence, modular programming, input validation, and statistical analysis without relying on external databases or complex GUI frameworks.

## Features

- **Automatic Persistence**: Saves and loads the account details and entire transaction history to and from a local JSON file (`account_data.json`).
- **Simulated Transfers**: Transfer funds safely to external accounts (validates recipient details and current balance).
- **Transaction History Filter**: Search and filter transaction logs by type (Deposits, Withdrawals, or Transfers).
- **Account Statement & Summary Metrics**: Displays comprehensive metrics including total deposits, total withdrawals, total transfers, and overall transaction counts.
- **Monthly Summary**: Groups all transaction activities by month (`YYYY-MM`), printing summary updates (deposits, outflows, net changes, and transaction frequencies).
- **Export to File**: Generates a clean text file `statement.txt` containing the full account details and formatted logs.
- **Strict Input Validation**: Checks name formatting (alphabetic and spaces only), numeric formats, account number digits, and enforces boundaries on negative/zero/overdraft amounts.
- **Professional Formatting**: All outputs are formatted with the Indian Rupee symbol (`₹`) and commas (e.g., `₹15,000.00`).

## OOP Concepts Used

1. **Classes and Objects**: Encapsulates account properties and transaction methods inside a single, modular `BankAccount` class.
2. **Encapsulation**: Enforces safe modifications to variables like `self.balance` through helper functions and object methods.
3. **Data Serialization**: Maps custom Python objects and `datetime` logs to standard JSON data formats for storage.

## Project Structure

```text
bank-account-class/
├── main.py
├── README.md
├── LICENSE
├── .gitignore
├── requirements.txt
├── account_data.json   # Auto-generated database storage file
└── statement.txt       # Auto-generated export statement
```

## How to Run

1. Make sure Python 3 is installed.
2. Open your terminal in the project directory.
3. Run the application:
   ```bash
   python main.py
   ```

## Example Usage

Here is a sample terminal session showing the application in action:

```text
Welcome back, Divyansh Kumar! Account loaded from database.

=====================================
      PERSONAL BANKING SIMULATOR     
=====================================
1. Deposit
2. Withdraw
3. Transfer Money
4. View Balance
5. Account Details
6. Transaction History
7. Monthly Summary
8. Export Statement
9. Exit
=====================================
Enter option (1-9): 5

=============================================
              ACCOUNT DETAILS                
=============================================
Account Holder       : Divyansh Kumar
Account Number       : 212121212
Current Balance      : ₹12,000.00
Total Deposits       : ₹15,000.00
Total Withdrawals    : ₹0.00
Total Transfers      : ₹3,000.00
Total Transactions   : 3
=============================================

=====================================
      PERSONAL BANKING SIMULATOR     
=====================================
...
Enter option (1-9): 7

=====================================================================
                          MONTHLY SUMMARY                            
=====================================================================
Month    | Deposited     | Withdrawn/Sent  | Net Change   | Tx Count
---------------------------------------------------------------------
2026-07  | ₹15,000.00    | ₹3,000.00       | +₹12,000.00  | 2       
=====================================================================
```

### Additional Account Examples

For multiple-user examples:

**Example 2:**
- **Account Holder**: Nashra
- **Account Number**: 101010101

**Example 3:**
- **Account Holder**: Meha
- **Account Number**: 103030303
