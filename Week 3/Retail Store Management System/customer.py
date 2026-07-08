"""
Customer Management Module for Retail Store Management System.

Handles operations relating to customer records, persistence, and loyalty updates.
"""

import os
import json
from models import Customer

class CustomerManager:
    """Manages customer registry, persistence, and search queries."""

    def __init__(self, data_file: str = "data/customers.json"):
        self.data_file = data_file
        self.customers = {}
        self.load_customers()

    def load_customers(self):
        """Loads customer data from the JSON file or initializes defaults if empty."""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        if not os.path.exists(self.data_file):
            self.create_default_customers()
            return

        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for cid, cdata in data.items():
                    self.customers[cid] = Customer.from_dict(cdata)
        except (json.JSONDecodeError, KeyError):
            self.create_default_customers()

    def save_customers(self):
        """Saves current customer state to the JSON file with human-readable formatting."""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        data = {cid: customer.to_dict() for cid, customer in self.customers.items()}
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def create_default_customers(self):
        """Populates default customer list on first run."""
        defaults = [
            Customer("CUST-1001", "Divyansh Kumar", "9876543210", "divyansh@example.com", loyalty_points=600, tier="Silver"),
            Customer("CUST-1002", "Rahul Verma", "9876543211", "rahul@example.com"),
            Customer("CUST-1003", "Priya Sharma", "9876543212", "priya@example.com"),
            Customer("CUST-1004", "Ananya Singh", "9876543213", "ananya@example.com")
        ]
        for c in defaults:
            self.customers[c.customer_id] = c
        self.save_customers()

    def register_customer(self, name: str, phone: str, email: str = "") -> tuple[bool, str, Customer | None]:
        """Registers a new customer after basic validation checks."""
        if not name.strip():
            return False, "Customer name cannot be empty.", None
        if not phone.strip() or len(phone) < 10 or not phone.isdigit():
            return False, "Invalid phone number. Must be at least 10 digits.", None

        # Check for duplicates by phone number
        for customer in self.customers.values():
            if customer.phone == phone:
                return False, f"Customer with phone {phone} already registered (ID: {customer.customer_id}).", None

        # Auto-generate Customer ID
        new_id_num = 1001
        if self.customers:
            existing_nums = []
            for cid in self.customers:
                try:
                    existing_nums.append(int(cid.split('-')[1]))
                except (IndexError, ValueError):
                    pass
            if existing_nums:
                new_id_num = max(existing_nums) + 1

        cust_id = f"CUST-{new_id_num}"
        new_cust = Customer(cust_id, name.strip(), phone.strip(), email.strip())
        self.customers[cust_id] = new_cust
        self.save_customers()
        return True, "Customer registered successfully.", new_cust

    def find_customer_by_phone(self, phone: str) -> Customer | None:
        """Finds a customer by phone number."""
        for customer in self.customers.values():
            if customer.phone == phone.strip():
                return customer
        return None

    def find_customer_by_id(self, customer_id: str) -> Customer | None:
        """Finds a customer by ID."""
        return self.customers.get(customer_id.upper().strip())

    def list_all_customers(self) -> list[Customer]:
        """Returns list of all registered customers."""
        return list(self.customers.values())
