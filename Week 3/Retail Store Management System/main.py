"""
Main CLI Module for Retail Store Management System.

Entry point providing interactive command-line menus for the business workflow,
error handling, and report outputs.
"""

import sys
import shutil
import os
from datetime import datetime
from inventory import InventoryManager
from customer import CustomerManager
from billing import BillingSystem, OfferEngine
from models import Cart

def print_header(title: str):
    """Prints a consistent section heading."""
    print("\n" + "=" * 55)
    print(title.upper().center(55))
    print("=" * 55)

def display_welcome_screen():
    """Displays startup branding information."""
    print("=" * 55)
    print("Retail Store Management System".center(55))
    print("Version 1.0.0".center(55))
    print("A modular command-line retail management application".center(55))
    print("built in Python using Object-Oriented Programming.".center(55))
    print("-" * 55)
    print("Features:")
    print("  ✔ Inventory Management   ✔ Customer Management")
    print("  ✔ Billing & Invoicing    ✔ Loyalty Program")
    print("  ✔ Smart Offers           ✔ Sales Analytics")
    print("  ✔ Profit Analysis        ✔ Inventory Tracking")
    print("  ✔ Reports                ✔ JSON Persistence")
    print("-" * 55)
    print("Author:".center(55))
    print("Divyansh Kumar".center(55))
    print("B.Tech Artificial Intelligence & Data Science".center(55))
    print("=" * 55 + "\n")

def display_dashboard(billing: BillingSystem):
    """Shows the startup retail dashboard statistics."""
    analytics = billing.get_sales_analytics()
    low_stock_list, out_stock_list = billing.inventory_mgr.get_stock_alerts(int(billing.settings["low_stock_threshold"]))
    cur = billing.settings["currency_symbol"]
    
    print("*" * 55)
    print(" RETAIL DASHBOARD ".center(55, "*"))
    print("*" * 55)
    print(f"  • Today's Revenue:       {cur}{analytics['today_revenue']:.2f}")
    print(f"  • Total Registered Cust: {len(billing.customer_mgr.customers)}")
    print(f"  • Products in Inventory: {len(billing.inventory_mgr.products)}")
    print(f"  • Low Stock Products:    {len(low_stock_list)} (Threshold: {billing.settings['low_stock_threshold']})")
    print(f"  • Out of Stock Products: {len(out_stock_list)}")
    print("*" * 55 + "\n")

def input_float(prompt: str, min_val: float = 0.0) -> float:
    """Helper to safely scan decimal numbers."""
    while True:
        try:
            val = float(input(prompt))
            if val < min_val:
                print(f"Error: Value must be at least {min_val}.")
                continue
            return val
        except ValueError:
            print("Error: Invalid numeric input. Please retry.")

def input_int(prompt: str, min_val: int = 0) -> int:
    """Helper to safely scan integers."""
    while True:
        try:
            val = int(input(prompt))
            if val < min_val:
                print(f"Error: Value must be at least {min_val}.")
                continue
            return val
        except ValueError:
            print("Error: Invalid integer input. Please retry.")

def manage_inventory(inv_mgr: InventoryManager):
    """Sub-menu for inventory management."""
    while True:
        print_header("Inventory Management")
        print("1. View Inventory Stock")
        print("2. Add New Product")
        print("3. Update Existing Product")
        print("4. Refill Stock")
        print("5. Delete Product")
        print("6. View Stock Alerts")
        print("7. View Inventory Movement History")
        print("8. Return to Main Menu")
        
        choice = input("\nSelect Option (1-8): ").strip()
        if choice == "1":
            print_header("Current Stock List")
            print(f"{'ID':<12} {'Product Name':<22} {'Category':<15} {'Cost':<8} {'Price':<8} {'Qty':<5}")
            print("-" * 70)
            for p in inv_mgr.products.values():
                print(f"{p.product_id:<12} {p.name[:21]:<22} {p.category[:14]:<15} ₹{p.cost_price:<7.2f} ₹{p.price:<7.2f} {p.quantity:<5}")
        elif choice == "2":
            print_header("Add New Product")
            pid = input("Enter Product ID (e.g. PROD-1009): ").strip().upper()
            name = input("Enter Product Name: ").strip()
            print(f"Categories: {', '.join(inv_mgr.categories)}")
            cat = input("Enter Category Name (or type new one): ").strip()
            cost = input_float("Enter Cost Price: ")
            price = input_float("Enter Selling Price: ")
            qty = input_int("Enter Initial Stock Quantity: ")
            success, msg = inv_mgr.add_product(pid, name, cat, cost, price, qty)
            print(msg)
        elif choice == "3":
            print_header("Update Product Attributes")
            pid = input("Enter Product ID to Update: ").strip().upper()
            if pid not in inv_mgr.products:
                print("Error: Product ID does not exist.")
                continue
            name = input("New Product Name (Press Enter to keep current): ").strip()
            cat = input("New Category Name (Press Enter to keep current): ").strip()
            cost_str = input("New Cost Price (Press Enter to keep current): ").strip()
            price_str = input("New Selling Price (Press Enter to keep current): ").strip()
            
            cost = float(cost_str) if cost_str else None
            price = float(price_str) if price_str else None
            success, msg = inv_mgr.update_product(pid, name, cat, cost, price)
            print(msg)
        elif choice == "4":
            print_header("Stock Refill")
            pid = input("Enter Product ID: ").strip().upper()
            qty = input_int("Enter Quantity to Add: ", 1)
            success, msg = inv_mgr.refill_stock(pid, qty)
            print(msg)
        elif choice == "5":
            print_header("Delete Product")
            pid = input("Enter Product ID to Delete: ").strip().upper()
            confirm = input(f"Are you sure you want to delete {pid}? (y/n): ").strip().lower()
            if confirm == "y":
                success, msg = inv_mgr.delete_product(pid)
                print(msg)
            else:
                print("Deletion cancelled.")
        elif choice == "6":
            print_header("Stock Alerts")
            threshold = input_int("Enter threshold value for low stock check: ", 1)
            low, out = inv_mgr.get_stock_alerts(threshold)
            print(f"\n[OUT OF STOCK] ({len(out)} items):")
            for p in out:
                print(f"  • {p.product_id}: {p.name} (0 left)")
            print(f"\n[LOW STOCK] ({len(low)} items):")
            for p in low:
                print(f"  • {p.product_id}: {p.name} ({p.quantity} left)")
        elif choice == "7":
            print_header("Inventory Movement History")
            history = inv_mgr.get_movement_history()
            if not history:
                print("No movement records found.")
            else:
                for idx, log in enumerate(reversed(history[-30:]), 1):
                    print(f"[{log['timestamp'][:19]}] {log['product_id']}: {log['action']} - {log['details']}")
        elif choice == "8":
            break
        else:
            print("Error: Invalid choice.")

def manage_customers(cust_mgr: CustomerManager):
    """Sub-menu for customer management."""
    while True:
        print_header("Customer Management")
        print("1. List All Customers")
        print("2. Register New Customer")
        print("3. Search Customer")
        print("4. Return to Main Menu")
        
        choice = input("\nSelect Option (1-4): ").strip()
        if choice == "1":
            print_header("Registered Customers")
            print(f"{'Customer ID':<13} {'Name':<20} {'Phone':<12} {'Loyalty Pts':<11} {'Tier':<8}")
            print("-" * 68)
            for c in cust_mgr.list_all_customers():
                print(f"{c.customer_id:<13} {c.name[:19]:<20} {c.phone:<12} {c.loyalty_points:<11} {c.tier:<8}")
        elif choice == "2":
            print_header("Register New Customer")
            name = input("Enter Full Name: ").strip()
            phone = input("Enter Phone Number: ").strip()
            email = input("Enter Email Address (optional): ").strip()
            success, msg, _ = cust_mgr.register_customer(name, phone, email)
            print(msg)
        elif choice == "3":
            print_header("Search Customer")
            query = input("Enter Phone or Customer ID: ").strip()
            c = cust_mgr.find_customer_by_phone(query) or cust_mgr.find_customer_by_id(query)
            if c:
                print(f"\nName:         {c.name}")
                print(f"Customer ID:  {c.customer_id}")
                print(f"Phone:        {c.phone}")
                print(f"Email:        {c.email or 'N/A'}")
                print(f"Loyalty Pts:  {c.loyalty_points}")
                print(f"Tier Level:   {c.tier}")
                print(f"Orders Placed: {len(c.purchase_history)}")
            else:
                print("Customer not found.")
        elif choice == "4":
            break
        else:
            print("Error: Invalid choice.")

def create_billing_transaction(billing: BillingSystem):
    """Workflow to generate a transaction bill."""
    print_header("Create Bill / Checkout")
    phone = input("Enter Customer Phone Number (or press Enter to skip lookup): ").strip()
    customer = None
    
    if phone:
        customer = billing.customer_mgr.find_customer_by_phone(phone)
        if not customer:
            print("Customer not registered.")
            reg = input("Register them now? (y/n): ").strip().lower()
            if reg == "y":
                name = input("Enter Customer Name: ").strip()
                email = input("Enter Email (optional): ").strip()
                success, msg, customer = billing.customer_mgr.register_customer(name, phone, email)
                print(msg)
            else:
                print("Proceeding as Walk-in Customer.")
    
    if not customer:
        customer = billing.customer_mgr.find_customer_by_id("CUST-1002") # Default guest user

    print(f"\nActive Billing Session for: {customer.name} (Tier: {customer.tier})")
    cart = Cart()

    while True:
        print(f"\nCart Items ({len(cart.items)} types loaded):")
        cur = billing.settings["currency_symbol"]
        sub, _ = cart.get_totals(billing.inventory_mgr.products)
        print(f"Current Cart Subtotal: {cur}{sub:.2f}")
        
        print("1. Add Product to Cart")
        print("2. Remove Product")
        print("3. Modify Quantity")
        print("4. Process Checkout & Pay")
        print("5. Cancel Transaction")
        
        choice = input("\nSelect checkout option: ").strip()
        if choice == "1":
            search = input("Enter Product name or ID to search: ").strip()
            matches = billing.inventory_mgr.search_products(search)
            if not matches:
                print("No matching products found.")
                continue
            
            print("\nMatching Products:")
            for idx, p in enumerate(matches, 1):
                print(f"  {idx}. {p.product_id} - {p.name} (Price: {cur}{p.price}, Available: {p.quantity})")
            
            select = input_int(f"Select option (1-{len(matches)}): ", 1)
            if select > len(matches):
                print("Invalid selection.")
                continue
            
            selected_product = matches[select - 1]
            qty = input_int(f"Enter Quantity to Add: ", 1)
            success, msg = cart.add_item(selected_product, qty)
            print(msg)
        elif choice == "2":
            pid = input("Enter Product ID to remove: ").strip().upper()
            success, msg = cart.remove_item(pid)
            print(msg)
        elif choice == "3":
            pid = input("Enter Product ID: ").strip().upper()
            if pid not in cart.items:
                print("Product not in cart.")
                continue
            p = billing.inventory_mgr.products.get(pid)
            qty = input_int("Enter New Quantity: ", 0)
            success, msg = cart.update_quantity(p, qty)
            print(msg)
        elif choice == "4":
            if not cart.items:
                print("Cart is empty.")
                continue
            
            # Offer Engine Recommendations
            eligible_offers = OfferEngine.get_eligible_offers(cart, customer, billing.inventory_mgr.products)
            applied_offer = None
            if eligible_offers:
                print("\n=== ELIGIBLE OFFERS ===")
                for idx, offer in enumerate(eligible_offers, 1):
                    print(f"  {idx}. Code: {offer['code']} - {offer['desc']}")
                print("  0. Do not apply discount codes")
                
                sel_off = input_int(f"Select discount (0-{len(eligible_offers)}): ", 0)
                if 0 < sel_off <= len(eligible_offers):
                    applied_offer = eligible_offers[sel_off - 1]
                    print(f"Offer {applied_offer['code']} selected.")
            
            # Preview Invoice
            sub, cost = cart.get_totals(billing.inventory_mgr.products)
            disc_amt = 0.0
            if applied_offer:
                val = float(applied_offer["value"])
                if applied_offer["type"] == "percent":
                    disc_amt = (sub * val) / 100.0
                else:
                    disc_amt = min(val, sub)
            
            taxable = max(0.0, sub - disc_amt)
            gst_pct = float(billing.settings["gst_rate"])
            gst_val = (taxable * gst_pct) / 100.0
            grand = taxable + gst_val
            
            print_header("Invoice Preview")
            print(f"Customer Name: {customer.name}")
            print(f"GST Rate Applied: {gst_pct}%")
            print(f"Subtotal:      {cur}{sub:.2f}")
            print(f"Discount:      -{cur}{disc_amt:.2f} ({applied_offer['code'] if applied_offer else 'None'})")
            print(f"GST:           {cur}{gst_val:.2f}")
            print(f"Grand Total:   {cur}{grand:.2f}")
            
            confirm = input("\nConfirm invoice checkout? (y/n): ").strip().lower()
            if confirm == "y":
                success, msg, inv = billing.checkout(cart, customer, applied_offer)
                print(msg)
                if success and inv:
                    print(f"Saved invoice text to reports/{inv['invoice_id']}.txt")
                break
            else:
                print("Checkout cancelled. Returning to cart.")
        elif choice == "5":
            print("Transaction cancelled.")
            break
        else:
            print("Invalid option.")

def view_sales_history(billing: BillingSystem):
    """Sub-menu for invoice lookups."""
    while True:
        print_header("Sales History & Invoice Lookup")
        print("1. View All Invoices (Summarized)")
        print("2. Search Invoice (By ID, Customer Name, or Date)")
        print("3. Filter Invoices (Today, Week, Month, All Time)")
        print("4. Return to Main Menu")
        
        choice = input("\nSelect Option (1-4): ").strip()
        cur = billing.settings["currency_symbol"]
        
        if choice == "1":
            print_header("Sales History Records")
            if not billing.sales_history:
                print("No sales recorded yet.")
                continue
            print(f"{'Invoice ID':<12} {'Date/Time':<20} {'Customer':<20} {'Amount':<10}")
            print("-" * 65)
            for inv in reversed(billing.sales_history):
                print(f"{inv['invoice_id']:<12} {inv['timestamp'][:16]:<20} {inv['customer_name'][:19]:<20} {cur}{inv['grand_total']:<9.2f}")
        elif choice == "2":
            q = input("Enter search term (e.g. INV-1001, Divyansh, or 2026-07): ").strip()
            results = billing.search_invoices(q)
            if not results:
                print("No invoices matched the search query.")
            else:
                print(f"\nFound {len(results)} matches:")
                for inv in results:
                    print(f"  • {inv['invoice_id']} | {inv['timestamp'][:16]} | {inv['customer_name']} | Total: {cur}{inv['grand_total']:.2f}")
        elif choice == "3":
            print("Choose filter period:")
            print("1. Today\n2. This Week\n3. This Month\n4. All Time")
            fil = input("Choice (1-4): ").strip()
            periods = {"1": "Today", "2": "This Week", "3": "This Month", "4": "All Time"}
            period = periods.get(fil, "All Time")
            
            results = billing.get_filtered_sales(period)
            print_header(f"Sales Filter: {period}")
            if not results:
                print(f"No invoices found for period '{period}'.")
            else:
                for inv in results:
                    print(f"  • {inv['invoice_id']} | {inv['timestamp'][:16]} | {inv['customer_name']} | Total: {cur}{inv['grand_total']:.2f}")
        elif choice == "4":
            break
        else:
            print("Invalid Option.")

def view_analytics_dashboard(billing: BillingSystem):
    """Renders business analytical outputs."""
    print_header("Sales Analytics Dashboard")
    analytics = billing.get_sales_analytics()
    cur = billing.settings["currency_symbol"]
    
    print(f"1. Total Sales Revenue:     {cur}{analytics['total_revenue']:.2f}")
    print(f"2. Total Profit Realized:   {cur}{analytics['total_profit']:.2f}")
    print(f"3. Net Profit Margin:       {analytics['profit_margin']:.2f}%")
    print(f"4. Total Orders Checked Out: {analytics['total_orders']}")
    print(f"5. Average Order Value:     {cur}{analytics['avg_order_value']:.2f}")
    print(f"6. Highest Single Invoice:  {cur}{analytics['highest_single_invoice']:.2f}")
    print("-" * 55)
    print(f"7. Best Selling Product:    {analytics['best_selling_product']}")
    print(f"8. Most Profitable Category:{analytics['most_profitable_category']}")
    print(f"9. Highest Revenue Category:{analytics['highest_revenue_category']}")
    print(f"10. Most Loyal Customer:    {analytics['most_loyal_customer']}")
    print("-" * 55)
    print("Top 5 Products Sold by Quantity:")
    for name, qty in analytics["top_5_products"]:
        print(f"  • {name}: {qty} units")
    print("-" * 55)
    print(f"Fast Moving (>=10 sales): {', '.join(analytics['fast_moving_products']) or 'None'}")
    print(f"Slow Moving (<3 sales):   {', '.join(analytics['slow_moving_products']) or 'None'}")

def generate_text_reports(billing: BillingSystem):
    """Outputs reports to flat txt files."""
    print_header("Report Generation Settings")
    print("1. Generate Daily Sales Report")
    print("2. Generate Inventory Status Report")
    print("3. Return to Main Menu")
    
    choice = input("\nSelect Option (1-3): ").strip()
    os.makedirs("reports", exist_ok=True)
    cur = billing.settings["currency_symbol"]
    timestamp_str = datetime.now().isoformat()[:19]
    
    if choice == "1":
        path = "reports/daily_sales_report.txt"
        sales = billing.get_filtered_sales("Today")
        revenue = sum(inv["grand_total"] for inv in sales if inv["status"] != "Cancelled")
        orders = len([inv for inv in sales if inv["status"] != "Cancelled"])
        
        lines = [
            "=" * 50,
            "DAILY SALES REPORT".center(50),
            f"Generated At: {timestamp_str}".center(50),
            "=" * 50,
            f"Total Orders Placed: {orders}",
            f"Total Revenue Generated Today: {cur}{revenue:.2f}",
            "-" * 50,
            f"{'Invoice ID':<15} {'Customer Name':<20} {'Grand Total':<12}",
            "-" * 50
        ]
        for inv in sales:
            lines.append(f"{inv['invoice_id']:<15} {inv['customer_name'][:19]:<20} {cur}{inv['grand_total']:<11.2f}")
        lines.append("=" * 50)
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write("\n".join(lines))
        print(f"Saved daily sales report to {path}")
    elif choice == "2":
        path = "reports/inventory_report.txt"
        lines = [
            "=" * 55,
            "INVENTORY STATUS REPORT".center(55),
            f"Generated At: {timestamp_str}".center(55),
            "=" * 55,
            f"{'ID':<12} {'Product Name':<20} {'Price':<10} {'Stock Qty':<10}",
            "-" * 55
        ]
        for p in billing.inventory_mgr.products.values():
            lines.append(f"{p.product_id:<12} {p.name[:19]:<20} {cur}{p.price:<9.2f} {p.quantity:<10}")
        lines.append("=" * 55)
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write("\n".join(lines))
        print(f"Saved inventory status report to {path}")

def manage_settings(billing: BillingSystem):
    """Alters settings key-values and writes modifications."""
    print_header("System Settings")
    for key, val in billing.settings.items():
        print(f"  • {key.replace('_', ' ').title()}: {val}")
    
    confirm = input("\nDo you want to edit settings? (y/n): ").strip().lower()
    if confirm == "y":
        billing.settings["store_name"] = input(f"Store Name [{billing.settings['store_name']}]: ").strip() or billing.settings["store_name"]
        billing.settings["store_address"] = input(f"Store Address [{billing.settings['store_address']}]: ").strip() or billing.settings["store_address"]
        billing.settings["store_phone"] = input(f"Store Phone [{billing.settings['store_phone']}]: ").strip() or billing.settings["store_phone"]
        billing.settings["welcome_msg"] = input(f"Welcome Message [{billing.settings['welcome_msg']}]: ").strip() or billing.settings["welcome_msg"]
        billing.settings["thank_you_msg"] = input(f"Thank You Message [{billing.settings['thank_you_msg']}]: ").strip() or billing.settings["thank_you_msg"]
        billing.settings["gst_rate"] = input_float(f"GST Rate [{billing.settings['gst_rate']}]: ")
        billing.settings["currency_symbol"] = input(f"Currency Symbol [{billing.settings['currency_symbol']}]: ").strip() or billing.settings["currency_symbol"]
        billing.settings["invoice_prefix"] = input(f"Invoice Prefix [{billing.settings['invoice_prefix']}]: ").strip().upper() or billing.settings["invoice_prefix"]
        billing.settings["low_stock_threshold"] = input_int(f"Low Stock Threshold [{billing.settings['low_stock_threshold']}]: ")
        
        billing.save_settings()
        print("Settings saved successfully.")

def backup_restore_data(billing: BillingSystem):
    """Sub-menu to backup/restore files."""
    print_header("Backup & Restore Data")
    print("1. Backup Data Files")
    print("2. Restore Data Files")
    print("3. Return to Main Menu")
    
    choice = input("\nSelect Option (1-3): ").strip()
    os.makedirs("data/backups", exist_ok=True)
    
    files_to_backup = [
        "data/products.json",
        "data/customers.json",
        "data/sales_history.json",
        "data/settings.json",
        "data/inventory_log.json"
    ]
    
    if choice == "1":
        for file in files_to_backup:
            if os.path.exists(file):
                shutil.copy2(file, f"data/backups/{os.path.basename(file)}")
        print("Backup created successfully in data/backups/ folder.")
    elif choice == "2":
        confirm = input("Are you sure you want to restore? This will overwrite active data. (y/n): ").strip().lower()
        if confirm == "y":
            restored = 0
            for file in files_to_backup:
                backup_path = f"data/backups/{os.path.basename(file)}"
                if os.path.exists(backup_path):
                    shutil.copy2(backup_path, file)
                    restored += 1
            if restored > 0:
                print("Restore completed. Reloading registry data...")
                billing.inventory_mgr.load_inventory()
                billing.customer_mgr.load_customers()
                billing.load_settings()
                billing.load_sales_history()
            else:
                print("No backups found to restore.")
        else:
            print("Restore operation cancelled.")

def main():
    """Main CLI shell execution loop."""
    display_welcome_screen()
    
    # Initialize Managers
    inv_mgr = InventoryManager()
    cust_mgr = CustomerManager()
    billing = BillingSystem(inv_mgr, cust_mgr)
    
    while True:
        display_dashboard(billing)
        print("=== MAIN MENU ===")
        print("1. Inventory Management")
        print("2. Create Bill / Checkout")
        print("3. View Sales History & Invoices")
        print("4. Sales Analytics Dashboard")
        print("5. Generate Reports")
        print("6. Settings")
        print("7. Backup & Restore Data")
        print("8. Exit Application")
        
        choice = input("\nSelect Option (1-8): ").strip()
        if choice == "1":
            manage_inventory(inv_mgr)
        elif choice == "2":
            create_billing_transaction(billing)
        elif choice == "3":
            view_sales_history(billing)
        elif choice == "4":
            view_analytics_dashboard(billing)
        elif choice == "5":
            generate_text_reports(billing)
        elif choice == "6":
            manage_settings(billing)
        elif choice == "7":
            backup_restore_data(billing)
        elif choice == "8":
            print("\nExiting. Thank you for using Retail Store Management System!")
            sys.exit(0)
        else:
            print("Error: Invalid selection. Try again.")

if __name__ == "__main__":
    main()
