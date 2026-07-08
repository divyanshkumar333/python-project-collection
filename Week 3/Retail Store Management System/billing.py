"""
Billing Module for Retail Store Management System.

Handles tax/GST, discount engine, checkout, sales reporting, and invoice persistence.
"""

import os
import json
from datetime import datetime, timedelta
from models import Product, Customer, Cart
from inventory import InventoryManager
from customer import CustomerManager

class OfferEngine:
    """Evaluates and suggests discounts based on cart contents, coupons, and customer profiles."""

    COUPONS = {
        "WELCOME10": {"type": "percent", "value": 10, "min_spend": 0, "desc": "10% off for first-time customers"},
        "SAVE500": {"type": "flat", "value": 500, "min_spend": 3000, "desc": "₹500 off on purchases above ₹3000"},
        "STUDENT5": {"type": "percent", "value": 5, "min_spend": 0, "desc": "5% Student Discount"}
    }

    @staticmethod
    def get_eligible_offers(cart: Cart, customer: Customer, products_dict: dict[str, Product]) -> list[dict]:
        """Scans cart/customer to compile list of eligible promo codes and automatic deals."""
        subtotal, _ = cart.get_totals(products_dict)
        offers = []

        # 1. Tier-based Loyalty Discount
        if customer.tier == "Gold":
            offers.append({
                "code": "GOLD10",
                "type": "percent",
                "value": 10.0,
                "desc": "Automatic 10% Loyalty Discount (Gold Tier)"
            })
        elif customer.tier == "Silver":
            offers.append({
                "code": "SILVER5",
                "type": "percent",
                "value": 5.0,
                "desc": "Automatic 5% Loyalty Discount (Silver Tier)"
            })

        # 2. Buy X Get Y Free (Buy 2 Get 1 Free on Books)
        book_qty = 0
        book_price = 0.0
        for pid, qty in cart.items.items():
            if pid in products_dict and products_dict[pid].category.lower() == "books":
                book_qty += qty
                book_price = products_dict[pid].price  # Approximate free item price
        if book_qty >= 2:
            free_units = book_qty // 2
            free_value = free_units * book_price
            offers.append({
                "code": "B2G1_BOOKS",
                "type": "flat",
                "value": free_value,
                "desc": f"Buy 2 Get 1 Free on Books (Saves ₹{free_value:.2f})"
            })

        # 3. Standard Coupons
        for code, details in OfferEngine.COUPONS.items():
            if subtotal >= details["min_spend"]:
                # Custom logic: WELCOME10 only if customer has no purchase history
                if code == "WELCOME10" and len(customer.purchase_history) > 0:
                    continue
                offers.append({
                    "code": code,
                    "type": details["type"],
                    "value": details["value"],
                    "desc": details["desc"]
                })

        # 4. Festival Discount (Flat 8% for everyone)
        offers.append({
            "code": "FESTIVAL8",
            "type": "percent",
            "value": 8.0,
            "desc": "Festival Special 8% discount on all items"
        })

        return offers


class BillingSystem:
    """Handles checkout execution, sales record lookup, reports, and analytical insights."""

    def __init__(self, inventory_mgr: InventoryManager, customer_mgr: CustomerManager,
                 sales_file: str = "data/sales_history.json", settings_file: str = "data/settings.json"):
        self.inventory_mgr = inventory_mgr
        self.customer_mgr = customer_mgr
        self.sales_file = sales_file
        self.settings_file = settings_file
        self.sales_history = []
        self.settings = {
            "store_name": "Apna Bazaar",
            "store_address": "Sector 62, Noida, UP - 201301",
            "store_phone": "0120-4567890",
            "welcome_msg": "Welcome to our store!",
            "thank_you_msg": "Thank you for shopping with us! Visit again.",
            "gst_rate": 18.0,
            "currency_symbol": "₹",
            "invoice_prefix": "INV",
            "low_stock_threshold": 3
        }
        self.load_settings()
        self.load_sales_history()

    def load_settings(self):
        """Loads store settings from JSON or creates defaults."""
        os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
        if not os.path.exists(self.settings_file):
            self.save_settings()
            return
        try:
            with open(self.settings_file, 'r', encoding='utf-8') as f:
                self.settings.update(json.load(f))
        except (json.JSONDecodeError, KeyError):
            self.save_settings()

    def save_settings(self):
        """Saves settings configuration to settings.json."""
        os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
        with open(self.settings_file, 'w', encoding='utf-8') as f:
            json.dump(self.settings, f, indent=4, ensure_ascii=False)

    def load_sales_history(self):
        """Loads purchase records from sales_history.json."""
        if not os.path.exists(self.sales_file):
            return
        try:
            with open(self.sales_file, 'r', encoding='utf-8') as f:
                self.sales_history = json.load(f)
        except (json.JSONDecodeError, ValueError):
            self.sales_history = []

    def save_sales_history(self):
        """Saves purchase history array back to JSON."""
        os.makedirs(os.path.dirname(self.sales_file), exist_ok=True)
        with open(self.sales_file, 'w', encoding='utf-8') as f:
            json.dump(self.sales_history, f, indent=4, ensure_ascii=False)

    def generate_invoice_id(self) -> str:
        """Auto-increments and formats the invoice number."""
        prefix = self.settings["invoice_prefix"]
        start_num = 1001
        if self.sales_history:
            nums = []
            for inv in self.sales_history:
                inv_id = inv.get("invoice_id", "")
                if inv_id.startswith(prefix + "-"):
                    try:
                        nums.append(int(inv_id.split("-")[1]))
                    except (IndexError, ValueError):
                        pass
            if nums:
                start_num = max(nums) + 1
        return f"{prefix}-{start_num}"

    def checkout(self, cart: Cart, customer: Customer, applied_offer: dict = None) -> tuple[bool, str, dict | None]:
        """Processes transaction details, performs math calculations, updates stock, and saves logs."""
        if not cart.items:
            return False, "Cannot checkout empty cart.", None

        subtotal, total_cost = cart.get_totals(self.inventory_mgr.products)
        discount_amount = 0.0

        if applied_offer:
            val = float(applied_offer["value"])
            if applied_offer["type"] == "percent":
                discount_amount = (subtotal * val) / 100.0
            else:
                discount_amount = min(val, subtotal)

        taxable_amt = max(0.0, subtotal - discount_amount)
        gst_pct = float(self.settings["gst_rate"])
        gst_amount = (taxable_amt * gst_pct) / 100.0
        grand_total = taxable_amt + gst_amount

        # Check stock again before finalizing
        for pid, qty in cart.items.items():
            p = self.inventory_mgr.products.get(pid)
            if not p or p.quantity < qty:
                return False, f"Stock for {p.name if p else pid} has changed. Transaction aborted.", None

        invoice_id = self.generate_invoice_id()
        timestamp = datetime.now().isoformat()

        # Update Stock quantities and log sales movements
        purchased_items = []
        for pid, qty in cart.items.items():
            p = self.inventory_mgr.products[pid]
            p.quantity -= qty
            self.inventory_mgr.log_movement(pid, "Product Sold", f"Sold {qty} units in invoice {invoice_id}.")
            purchased_items.append({
                "product_id": pid,
                "name": p.name,
                "category": p.category,
                "price": p.price,
                "cost_price": p.cost_price,
                "quantity": qty,
                "total": p.price * qty
            })
        self.inventory_mgr.save_inventory()

        # Update Customer Loyalty metrics (1 point for every ₹100 spent)
        points_earned = int(grand_total // 100)
        customer.add_loyalty_points(points_earned)
        customer.purchase_history.append(invoice_id)
        self.customer_mgr.save_customers()

        invoice = {
            "invoice_id": invoice_id,
            "timestamp": timestamp,
            "customer_id": customer.customer_id,
            "customer_name": customer.name,
            "customer_phone": customer.phone,
            "items": purchased_items,
            "subtotal": subtotal,
            "discount_code": applied_offer["code"] if applied_offer else "None",
            "discount_amount": discount_amount,
            "gst_rate": gst_pct,
            "gst_amount": gst_amount,
            "grand_total": grand_total,
            "total_cost": total_cost,
            "points_earned": points_earned,
            "status": "Paid"
        }

        self.sales_history.append(invoice)
        self.save_sales_history()
        self.write_invoice_to_text(invoice)

        return True, f"Transaction checked out successfully under ID: {invoice_id}", invoice

    def write_invoice_to_text(self, invoice: dict) -> str:
        """Writes invoice output in formatted text layout to reports/ folder."""
        os.makedirs("reports", exist_ok=True)
        filepath = f"reports/{invoice['invoice_id']}.txt"
        cur = self.settings["currency_symbol"]

        lines = [
            "=" * 50,
            self.settings["store_name"].center(50),
            self.settings["store_address"].center(50),
            f"Phone: {self.settings['store_phone']}".center(50),
            "=" * 50,
            f"Invoice: {invoice['invoice_id']}".ljust(25) + f"Status: {invoice['status']}".rjust(25),
            f"Date: {invoice['timestamp'][:19]}",
            f"Customer: {invoice['customer_name']} ({invoice['customer_phone']})",
            "-" * 50,
            f"{'Item Description':<25} {'Qty':<5} {'Price':<8} {'Total':<10}",
            "-" * 50
        ]

        for item in invoice["items"]:
            lines.append(f"{item['name'][:24]:<25} {item['quantity']:<5} {cur}{item['price']:<7.2f} {cur}{item['total']:<9.2f}")

        lines.extend([
            "-" * 50,
            f"Subtotal:".ljust(35) + f"{cur}{invoice['subtotal']:>13.2f}",
            f"Discount ({invoice['discount_code']}):".ljust(35) + f"-{cur}{invoice['discount_amount']:>12.2f}",
            f"GST ({invoice['gst_rate']}%):".ljust(35) + f"{cur}{invoice['gst_amount']:>13.2f}",
            "-" * 50,
            f"Grand Total:".ljust(35) + f"{cur}{invoice['grand_total']:>13.2f}",
            f"Loyalty Points Gained: {invoice['points_earned']}",
            "=" * 50,
            self.settings["welcome_msg"].center(50),
            self.settings["thank_you_msg"].center(50),
            "=" * 50
        ])

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("\n".join(lines))
        return filepath

    def search_invoices(self, query: str) -> list[dict]:
        """Searches invoices by invoice ID, customer name, or ISO date string."""
        q = query.lower().strip()
        results = []
        for inv in self.sales_history:
            if (q in inv["invoice_id"].lower() or 
                q in inv["customer_name"].lower() or 
                q in inv["timestamp"].lower()):
                results.append(inv)
        return results

    def get_filtered_sales(self, period: str) -> list[dict]:
        """Filters sales history by Today, This Week, This Month, or All Time."""
        now = datetime.now()
        filtered = []
        for inv in self.sales_history:
            try:
                dt = datetime.fromisoformat(inv["timestamp"])
            except ValueError:
                continue

            if period == "Today":
                if dt.date() == now.date():
                    filtered.append(inv)
            elif period == "This Week":
                if now - dt <= timedelta(days=7):
                    filtered.append(inv)
            elif period == "This Month":
                if dt.year == now.year and dt.month == now.month:
                    filtered.append(inv)
            else:
                filtered.append(inv)
        return filtered

    def get_sales_analytics(self) -> dict:
        """Computes system metrics, revenue, cost, profit, velocity, and customer loyalty."""
        total_revenue = sum(inv["grand_total"] for inv in self.sales_history if inv["status"] != "Cancelled")
        total_cost = sum(inv["total_cost"] for inv in self.sales_history if inv["status"] != "Cancelled")
        total_profit = total_revenue - total_cost
        total_orders = len([inv for inv in self.sales_history if inv["status"] != "Cancelled"])
        avg_order = (total_revenue / total_orders) if total_orders > 0 else 0.0

        today_revenue = sum(inv["grand_total"] for inv in self.get_filtered_sales("Today") if inv["status"] != "Cancelled")

        # Calculations for product metrics
        product_sales_qty = {}
        category_revenue = {}
        category_cost = {}
        for inv in self.sales_history:
            if inv["status"] == "Cancelled":
                continue
            for item in inv["items"]:
                pid = item["product_id"]
                name = item["name"]
                cat = item["category"]
                qty = item["quantity"]
                total = item["total"]
                cost = item.get("cost_price", 0.0) * qty

                product_sales_qty[name] = product_sales_qty.get(name, 0) + qty
                category_revenue[cat] = category_revenue.get(cat, 0.0) + total
                category_cost[cat] = category_cost.get(cat, 0.0) + cost

        # Top sold product
        best_selling = max(product_sales_qty, key=product_sales_qty.get) if product_sales_qty else "N/A"
        
        # Most profitable category
        most_profitable_cat = "N/A"
        max_cat_profit = -1.0
        for cat in category_revenue:
            profit = category_revenue[cat] - category_cost.get(cat, 0.0)
            if profit > max_cat_profit:
                max_cat_profit = profit
                most_profitable_cat = cat

        # Top 5 products
        sorted_products = sorted(product_sales_qty.items(), key=lambda x: x[1], reverse=True)[:5]

        # Highest Revenue Category
        highest_rev_cat = max(category_revenue, key=category_revenue.get) if category_revenue else "N/A"

        # Most loyal/frequent customer
        customer_visits = {}
        for inv in self.sales_history:
            if inv["status"] != "Cancelled":
                name = inv["customer_name"]
                customer_visits[name] = customer_visits.get(name, 0) + 1
        most_loyal_cust = max(customer_visits, key=customer_visits.get) if customer_visits else "N/A"

        # Highest invoice amount
        highest_invoice = 0.0
        for inv in self.sales_history:
            if inv["status"] != "Cancelled" and inv["grand_total"] > highest_invoice:
                highest_invoice = inv["grand_total"]

        # Fast moving and slow moving products
        fast_moving = [name for name, qty in product_sales_qty.items() if qty >= 10]
        all_inventory_names = {p.name for p in self.inventory_mgr.products.values()}
        sold_names = set(product_sales_qty.keys())
        never_sold = list(all_inventory_names - sold_names)
        slow_moving = [name for name, qty in product_sales_qty.items() if qty < 3] + never_sold

        return {
            "total_revenue": total_revenue,
            "total_profit": total_profit,
            "profit_margin": (total_profit / total_revenue * 100) if total_revenue > 0 else 0.0,
            "today_revenue": today_revenue,
            "total_orders": total_orders,
            "avg_order_value": avg_order,
            "best_selling_product": best_selling,
            "highest_revenue_category": highest_rev_cat,
            "most_profitable_category": most_profitable_cat,
            "top_5_products": sorted_products,
            "most_loyal_customer": most_loyal_cust,
            "highest_single_invoice": highest_invoice,
            "fast_moving_products": fast_moving[:5],
            "slow_moving_products": slow_moving[:5],
            "never_sold_products": never_sold[:5]
        }
