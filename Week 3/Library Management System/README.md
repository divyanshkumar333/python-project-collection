# Library Management System

A professional, modular command-line Library Management System built using Object-Oriented Programming (OOP) in Python. This project is designed to demonstrate clean code architecture, JSON database persistence, business rules (such as fine calculation and due dates), and basic analytics.

## Project Overview

This application simulates a real-world library catalog system where library staff can manage books, register members, track borrowings, log activities, calculate overdue fines, and run reports. 

Developed as part of a B.Tech Artificial Intelligence & Data Science student portfolio to demonstrate software design fundamentals, serialization, and clean architectural separation.

---

## OOP Design & Class Diagram

The application uses standard Python modules to enforce separation of concerns:
- **`Book` (`models.py`)**: Models attributes of physical books, state representation, and serialization/deserialization.
- **`Member` (`models.py`)**: Models user profiles, their history, and active borrowings.
- **`Library` (`library.py`)**: Serves as the database controller and business logic orchestrator.

### Text-Based Class Diagram

```
+-------------------------------------------------------+
|                        Book                           |
+-------------------------------------------------------+
| - book_id: str                                        |
| - title: str                                          |
| - author: str                                         |
| - category: str                                       |
| - is_available: bool                                  |
+-------------------------------------------------------+
| + to_dict() -> dict                                   |
| + from_dict(data: dict) -> Book                       |
+-------------------------------------------------------+
                           ^
                           | manages
+--------------------------+----------------------------+
|                       Library                         |
+-------------------------------------------------------+
| - file_path: str                                      |
| - books: dict[str, Book]                              |
| - members: dict[str, Member]                          |
| - transactions: list[dict]                            |
| - categories: list[str]                               |
| - settings: dict                                      |
+-------------------------------------------------------+
| + add_book() / remove_book() / update_book()          |
| + register_member()                                   |
| + issue_book() / return_book()                        |
| + calculate_fine(due_date) -> int                     |
| + get_recommendations(category) -> list[Book]         |
| + get_statistics() -> dict                            |
| + export_report(filepath)                             |
+-------------------------------------------------------+
                           | manages
                           v
+-------------------------------------------------------+
|                       Member                          |
+-------------------------------------------------------+
| - member_id: str                                      |
| - name: str                                           |
| - borrowed_books: dict[str, str] (book_id -> due_date)|
| - borrowing_history: list[str]                        |
+-------------------------------------------------------+
| + to_dict() -> dict                                   |
| + from_dict(data: dict) -> Member                     |
+-------------------------------------------------------+
```

---

## Features

1. **Smart Dashboard**: Instantly views current statistics (total, available, and issued books, registered members, and overdue count) on boot.
2. **Book & Category Management**: Dynamic cataloging featuring user-defined categories.
3. **Member Management**: Detailed records showing borrower profiles, current loans, and borrowing history.
4. **Transaction Logging**: Preserves library transaction logs (issue, returns, new registers) inside `library.json`.
5. **Overdue Checks & Fines**: Auto-calculates late return fines at ₹10/day for books returned past their 14-day limit.
6. **Search & Recommendation Engine**: Searches books via partial match criteria and lists category-based recommendations.
7. **Reading Analytics**: Evaluates metrics like top book, most popular category, most active member, and average borrow duration.
8. **Report Generation**: Exports detailed reports directly to `library_report.txt`.

---

## Folder Structure

```
library-management-system/
│
├── main.py             # Entrypoint and CLI View Controller
├── library.py          # Controller Layer & Business Logic
├── models.py           # Data Models (Book & Member)
├── library.json        # JSON Database Storage
├── library_report.txt  # Exported System Report
├── requirements.txt    # Project Dependencies (None required)
├── .gitignore          # Git Ignored Files
├── LICENSE             # MIT License
└── README.md           # Documentation
```

---

## Installation & How to Run

1. Clone or copy the project files to your local directory.
2. Ensure you have Python 3.6+ installed.
3. Execute the entry point script using terminal or PowerShell:
   ```bash
   python main.py
   ```

---

## Example Dashboard Output

```
========================================
           Library Dashboard
========================================
  Total Books Registered  : 5
  Available Books         : 4
  Issued Books            : 1
  Registered Members      : 4
  Overdue Books           : 1
========================================
```

---

## Future Improvements

- Add a search filtering index for instantaneous queries over large catalogs.
- Develop unit tests for logic coverage across edge loan cases.
- Transition JSON structure into relational storage (e.g. SQLite) when database integration is authorized.
