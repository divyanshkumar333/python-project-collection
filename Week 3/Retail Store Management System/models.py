"""
Models Module for Retail Store Management System.

Contains domain classes representing Product, Customer, and Cart entities.
"""

class Product:
    """Represents a product in the retail store inventory."""

    def __init__(self, product_id: str, name: str, category: str, cost_price: float, price: float, quantity: int):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.cost_price = cost_price
        self.price = price
        self.quantity = quantity

    def to_dict(self) -> dict:
        """Converts the product object to a dictionary for JSON serialization."""
        return {
            "product_id": self.product_id,
            "name": self.name,
            "category": self.category,
            "cost_price": self.cost_price,
            "price": self.price,
            "quantity": self.quantity
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Product':
        """Creates a Product object from a dictionary."""
        return cls(
            product_id=data["product_id"],
            name=data["name"],
            category=data["category"],
            cost_price=float(data["cost_price"]),
            price=float(data["price"]),
            quantity=int(data["quantity"])
        )


class Customer:
    """Represents a customer and manages their loyalty profile."""

    TIERS = {
        "Bronze": 0,
        "Silver": 500,
        "Gold": 1500
    }

    def __init__(self, customer_id: str, name: str, phone: str, email: str = "",
                 purchase_history: list = None, loyalty_points: int = 0, tier: str = "Bronze"):
        self.customer_id = customer_id
        self.name = name
        self.phone = phone
        self.email = email
        self.purchase_history = purchase_history or []
        self.loyalty_points = loyalty_points
        self.tier = tier

    def add_loyalty_points(self, points: int):
        """Adds points and checks for loyalty tier upgrades."""
        self.loyalty_points += points
        self.update_tier()

    def update_tier(self):
        """Updates membership tier based on total loyalty points accumulated."""
        if self.loyalty_points >= self.TIERS["Gold"]:
            self.tier = "Gold"
        elif self.loyalty_points >= self.TIERS["Silver"]:
            self.tier = "Silver"
        else:
            self.tier = "Bronze"

    def to_dict(self) -> dict:
        """Converts customer object to a dictionary for serialization."""
        return {
            "customer_id": self.customer_id,
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "purchase_history": self.purchase_history,
            "loyalty_points": self.loyalty_points,
            "tier": self.tier
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Customer':
        """Creates a Customer object from a dictionary."""
        return cls(
            customer_id=data["customer_id"],
            name=data["name"],
            phone=data["phone"],
            email=data.get("email", ""),
            purchase_history=data.get("purchase_history", []),
            loyalty_points=data.get("loyalty_points", 0),
            tier=data.get("tier", "Bronze")
        )


class Cart:
    """Manages temporary items selected for check-out."""

    def __init__(self):
        # Maps product_id -> quantity
        self.items = {}

    def add_item(self, product: Product, quantity: int) -> tuple[bool, str]:
        """Adds an item or increments its quantity after validating stock."""
        if quantity <= 0:
            return False, "Quantity must be greater than zero."
        
        current_qty = self.items.get(product.product_id, 0)
        target_qty = current_qty + quantity
        
        if target_qty > product.quantity:
            return False, f"Insufficient stock. Available: {product.quantity}, Cart has: {current_qty}."

        self.items[product.product_id] = target_qty
        return True, "Item added to cart."

    def remove_item(self, product_id: str) -> tuple[bool, str]:
        """Removes an item completely from the cart."""
        if product_id in self.items:
            del self.items[product_id]
            return True, "Item removed from cart."
        return False, "Item not found in cart."

    def update_quantity(self, product: Product, quantity: int) -> tuple[bool, str]:
        """Overwrites the quantity of an item in the cart, checking stock."""
        if quantity <= 0:
            return self.remove_item(product.product_id)
        
        if quantity > product.quantity:
            return False, f"Insufficient stock. Available: {product.quantity}."

        self.items[product.product_id] = quantity
        return True, "Cart quantity updated."

    def clear(self):
        """Clears all items in the cart."""
        self.items.clear()

    def get_totals(self, products_dict: dict[str, Product]) -> tuple[float, float]:
        """Calculates total selling price (revenue) and total cost price for profit metrics."""
        subtotal = 0.0
        total_cost = 0.0
        for pid, qty in self.items.items():
            if pid in products_dict:
                p = products_dict[pid]
                subtotal += p.price * qty
                total_cost += p.cost_price * qty
        return subtotal, total_cost
