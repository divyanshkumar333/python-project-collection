"""
Inventory Management Module for Retail Store Management System.

Handles inventory operations including product CRUD, categorization, stock level alerts,
and logging of inventory movements.
"""

import os
import json
from datetime import datetime
from models import Product

class InventoryManager:
    """Manages store inventory, custom categories, stock adjustments, and log tracking."""

    def __init__(self, products_file: str = "data/products.json", log_file: str = "data/inventory_log.json"):
        self.products_file = products_file
        self.log_file = log_file
        self.products = {}
        self.categories = {"Grocery", "Electronics", "Clothing", "Books", "Accessories", "Home Appliances"}
        self.load_inventory()

    def load_inventory(self):
        """Loads inventory from products.json or loads defaults if the file is missing/empty."""
        os.makedirs(os.path.dirname(self.products_file), exist_ok=True)
        if not os.path.exists(self.products_file):
            self.create_default_inventory()
            return

        try:
            with open(self.products_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for pid, pdata in data.items():
                    p = Product.from_dict(pdata)
                    self.products[pid] = p
                    self.categories.add(p.category)
        except (json.JSONDecodeError, KeyError):
            self.create_default_inventory()

    def save_inventory(self):
        """Saves current inventory state to the JSON file with pretty formatting."""
        os.makedirs(os.path.dirname(self.products_file), exist_ok=True)
        data = {pid: p.to_dict() for pid, p in self.products.items()}
        with open(self.products_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def log_movement(self, product_id: str, action: str, details: str):
        """Logs an inventory transaction with an ISO timestamp."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "product_id": product_id,
            "action": action,
            "details": details
        }
        
        logs = []
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            except (json.JSONDecodeError, ValueError):
                pass
        
        logs.append(log_entry)
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(logs, f, indent=4, ensure_ascii=False)

    def create_default_inventory(self):
        """Creates sample inventory entries on first startup."""
        defaults = [
            Product("PROD-1001", "Rice", "Grocery", 40.0, 60.0, 50),
            Product("PROD-1002", "Milk", "Grocery", 25.0, 35.0, 30),
            Product("PROD-1003", "Keyboard", "Electronics", 800.0, 1200.0, 15),
            Product("PROD-1004", "Mouse", "Electronics", 200.0, 400.0, 20),
            Product("PROD-1005", "SSD", "Electronics", 2500.0, 3500.0, 2),
            Product("PROD-1006", "Python Programming Book", "Books", 300.0, 450.0, 12),
            Product("PROD-1007", "Laptop", "Electronics", 35000.0, 45000.0, 5),
            Product("PROD-1008", "Headphones", "Accessories", 1200.0, 1800.0, 8)
        ]
        for p in defaults:
            self.products[p.product_id] = p
            self.categories.add(p.category)
        self.save_inventory()
        for p in defaults:
            self.log_movement(p.product_id, "Product Added", f"Initial stock setup: {p.quantity} units.")

    def add_product(self, product_id: str, name: str, category: str, cost_price: float, price: float, quantity: int) -> tuple[bool, str]:
        """Validates and registers a new product in the store database."""
        pid_clean = product_id.upper().strip()
        name_clean = name.strip()
        cat_clean = category.strip()

        if not pid_clean or not name_clean or not cat_clean:
            return False, "ID, Name, and Category cannot be empty."
        if pid_clean in self.products:
            return False, f"Duplicate Product ID: {pid_clean} already exists."
        if cost_price < 0 or price < 0:
            return False, "Prices cannot be negative."
        if cost_price > price:
            return False, "Cost price cannot exceed selling price (cannot sell at loss on list price)."
        if quantity < 0:
            return False, "Stock quantity cannot be negative."

        new_product = Product(pid_clean, name_clean, cat_clean, cost_price, price, quantity)
        self.products[pid_clean] = new_product
        self.categories.add(cat_clean)
        self.save_inventory()
        self.log_movement(pid_clean, "Product Added", f"Added new product: {name_clean} in category {cat_clean}.")
        return True, f"Product {name_clean} added successfully."

    def update_product(self, product_id: str, name: str = None, category: str = None,
                       cost_price: float = None, price: float = None) -> tuple[bool, str]:
        """Modifies attributes of an existing product."""
        pid_clean = product_id.upper().strip()
        if pid_clean not in self.products:
            return False, f"Product {pid_clean} not found."
        
        p = self.products[pid_clean]
        changes = []

        if name and name.strip():
            p.name = name.strip()
            changes.append(f"Name to {p.name}")
        if category and category.strip():
            p.category = category.strip()
            self.categories.add(p.category)
            changes.append(f"Category to {p.category}")
        if cost_price is not None:
            if cost_price < 0:
                return False, "Cost price cannot be negative."
            p.cost_price = cost_price
            changes.append(f"Cost Price to {p.cost_price}")
        if price is not None:
            if price < 0:
                return False, "Selling price cannot be negative."
            p.price = price
            changes.append(f"Selling Price to {p.price}")

        if p.cost_price > p.price:
            return False, "Cost price cannot exceed selling price after update."

        self.save_inventory()
        if changes:
            self.log_movement(pid_clean, "Product Updated", f"Modified: {', '.join(changes)}")
        return True, "Product updated successfully."

    def refill_stock(self, product_id: str, added_qty: int) -> tuple[bool, str]:
        """Refills stock for an existing product and logs the event."""
        pid_clean = product_id.upper().strip()
        if pid_clean not in self.products:
            return False, "Product not found."
        if added_qty <= 0:
            return False, "Refill quantity must be greater than zero."

        p = self.products[pid_clean]
        p.quantity += added_qty
        self.save_inventory()
        self.log_movement(pid_clean, "Stock Refilled", f"Added {added_qty} units. New balance: {p.quantity}.")
        return True, f"Stock refilled successfully. Total: {p.quantity}."

    def delete_product(self, product_id: str) -> tuple[bool, str]:
        """Removes a product from the database."""
        pid_clean = product_id.upper().strip()
        if pid_clean not in self.products:
            return False, "Product not found."
        
        deleted_name = self.products[pid_clean].name
        del self.products[pid_clean]
        self.save_inventory()
        self.log_movement(pid_clean, "Product Deleted", f"Removed {deleted_name} from inventory.")
        return True, f"Product {deleted_name} deleted successfully."

    def search_products(self, query: str) -> list[Product]:
        """Searches products by ID, name, or category (case-insensitive)."""
        q = query.lower().strip()
        results = []
        for p in self.products.values():
            if q in p.product_id.lower() or q in p.name.lower() or q in p.category.lower():
                results.append(p)
        return results

    def add_custom_category(self, category_name: str) -> tuple[bool, str]:
        """Adds a custom category to the category pool."""
        cat_clean = category_name.strip()
        if not cat_clean:
            return False, "Category name cannot be empty."
        if cat_clean in self.categories:
            return True, f"Category '{cat_clean}' already exists."
        self.categories.add(cat_clean)
        return True, f"Category '{cat_clean}' registered."

    def get_stock_alerts(self, threshold: int) -> tuple[list[Product], list[Product]]:
        """Returns low stock list and out of stock list."""
        low_stock = []
        out_of_stock = []
        for p in self.products.values():
            if p.quantity == 0:
                out_of_stock.append(p)
            elif p.quantity <= threshold:
                low_stock.append(p)
        return low_stock, out_of_stock

    def get_movement_history(self) -> list[dict]:
        """Retrieves complete inventory movement history logs."""
        if not os.path.exists(self.log_file):
            return []
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, ValueError):
            return []
