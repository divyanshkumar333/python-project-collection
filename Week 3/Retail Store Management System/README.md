# Retail Store Management System

**Version 1.0.0**

A modular, clean, command-line retail billing and inventory management application built in Python using Object-Oriented Programming (OOP) principles.

---

## Project Overview

This Retail Store Management System is designed to simulate a real-world checkout and inventory operation for a retail store. The project exhibits clean design, modular code structure, and data persistence using standard JSON formats. It handles product inventory, customer registration, loyalty tracking, smart promotional rules, checkout flow with invoice preview, PDF-like formatted text invoices, historical reporting, and interactive analytics.

Developed by a motivated B.Tech Artificial Intelligence & Data Science student.

---

## Features

- **Inventory Management**: Full product CRUD with custom categories, cost/selling price metrics, and stock alerts.
- **Customer Management**: Membership registrations and lookup with a fully-integrated loyalty tier upgrade program (Bronze, Silver, Gold).
- **Billing & Invoicing**: Interactive cart operations, automatic GST calculation, invoice status tracking (`Paid`, `Pending`, `Cancelled`), and invoice preview confirmations.
- **Smart Offers Engine**: Built-in promotional rule analyzer that suggests eligible coupons (e.g. `WELCOME10`, `SAVE500`, `STUDENT5`), category discounts (Buy 2 Get 1 Free on Books), and loyalty tier discounts.
- **Analytics & Insights**: Complete metrics for business growth including total revenue, profits, margins, and sales velocity tracking.
- **Persistence & Portability**: Backup and restore functionalities without external SQL databases, relying on human-readable JSON files.
- **Structured Reporting**: Auto-exports individual text invoice records to the `reports/` folder, alongside printable daily sales and inventory status reports.

---

## Folder Structure

```text
billing-system/
│
├── main.py              # CLI Entry point & menus
├── models.py            # Entities: Product, Customer, Cart
├── inventory.py         # InventoryManager & Stock Movement Logger
├── customer.py          # CustomerManager
├── billing.py           # BillingSystem & OfferEngine
│
├── data/                # Database Folder (JSON files)
│   ├── products.json
│   ├── customers.json
│   ├── sales_history.json
│   ├── settings.json
│   └── inventory_log.json
│
├── reports/             # Invoice records & exports
│   ├── INV-1001.txt
│   ├── daily_sales_report.txt
│   └── inventory_report.txt
│
├── README.md            # Project description & documentation
├── LICENSE              # MIT License
├── requirements.txt     # Python dependency file (None required)
└── .gitignore           # Ignored temporary file mappings
```

---

## Architecture Diagram (Text-based)

```text
+-------------------------------------------------------------+
|                           main.py                           |
|        - Handles CLI input / output loop                    |
|        - Directs users to sub-menus and dashboard views     |
+------------------------------+------------------------------+
                               |
                               v
+------------------------------+------------------------------+
|                         billing.py                          |
|  +-------------------------------------------------------+  |
|  |                    BillingSystem                      |  |
|  | - Performs checkout validations                       |  |
|  | - Saves sales history records and writes text files   |  |
|  +---------------------------+---------------------------+  |
|                              |                               |
|                              v (Consults promo rules)        |
|  +---------------------------+---------------------------+  |
|  |                     OfferEngine                       |  |
|  | - Calculates coupon validity and tier loyalty         |  |
|  +-------------------------------------------------------+  |
+---------+--------------------+---------------------+--------+
          |                    |                     |
          v                    v                     v
+---------+----------+  +------+-----------+  +------+--------+
|    inventory.py    |  |   customer.py    |  |   models.py   |
| - Manages products |  | - Manages client |  | - Product     |
| - Logs movements   |  |   profiles/tiers |  | - Customer    |
| - Alerts low stock |  | - Saves client   |  | - Cart        |
| - JSON storage     |  |   JSON file      |  |               |
+--------------------+  +------------------+  +---------------+
```

---

## Technologies Used

- **Python 3**: Written strictly in Python 3 utilizing standard libraries only (`os`, `sys`, `json`, `datetime`, `shutil`).
- **JSON Storage**: Human-readable, structured, indented file persistence.

---

## Installation & How to Run

### Installation
Clone this repository to your local directory.
```bash
git clone <repository_url>
cd billing-system
```
*Note: There are no third-party libraries needed. `requirements.txt` is intentionally left empty.*

### How to Run
Run the application using Python:
```bash
python main.py
```

---

## Sample Invoice

```text
==================================================
                   Apna Bazaar                    
          Sector 62, Noida, UP - 201301           
                Phone: 0120-4567890               
==================================================
Invoice: INV-1001                     Status: Paid
Date: 2026-07-08T00:55:00
Customer: Divyansh Kumar (9876543210)
--------------------------------------------------
Item Description          Qty   Price    Total     
--------------------------------------------------
Python Programming Book   2     ₹450.00  ₹900.00   
Laptop                    1     ₹45000.00 ₹45000.00 
--------------------------------------------------
Subtotal:                             ₹45900.00
Discount (SAVE500):                    -₹500.00
GST (18.0%):                           ₹8172.00
--------------------------------------------------
Grand Total:                          ₹53572.00
Loyalty Points Gained: 535
==================================================
              Welcome to our store!               
       Thank you for shopping with us! Visit again.       
==================================================
```

---

## Learning Outcomes

- **Object-Oriented Programming (OOP)**: Realized encapsulation and modular design by separating models, inventory, customer registry, and payment processing.
- **Relational Integrity in Files**: Maintained references between client records and sales history without a relational database.
- **Data Validation & Business Logic**: Implemented edge-case validation checks (e.g. quantity limits, negative price exceptions, stock checks, and coupon dependencies).
- **Analytics Engineering**: Derived metrics like net margin, category profitability, and sales velocity logs programmatically.

---

## Future Improvements

1. **Credit / Pending Dues Management**: Allow tracking pending invoice statuses with credit limits.
2. **Barcode Scanner Integration**: Implement barcode input interface in CLI.
3. **Advanced CSV/Excel Export**: Add exports for financial audits.

---

## Author
**Divyansh Kumar**  
B.Tech Artificial Intelligence & Data Science
