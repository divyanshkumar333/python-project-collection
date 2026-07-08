import json
import os
import math
from datetime import datetime

class Calculator:
    """
    Main Calculator core that manages state, math operations,
    history/favorites file persistence, precision, and reports.
    """
    def __init__(self, history_file: str = "history.json"):
        self.history_file = history_file
        self.memory = 0.0
        self.precision = 4  # Default decimal precision
        self.session_history = []  # Tracks operations performed in current run
        self.history = []
        self.favorites = []
        
        self.load_data()

    def load_data(self):
        """Loads calculation history and favorites from the JSON file."""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.history = data.get("history", [])
                    self.favorites = data.get("favorites", [])
            except (json.JSONDecodeError, KeyError):
                # Fallback if file is corrupted
                self.history = []
                self.favorites = []
        else:
            self.history = []
            self.favorites = []

    def save_data(self):
        """Saves current history and favorites to the JSON file."""
        data = {
            "history": self.history,
            "favorites": self.favorites
        }
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
        except IOError as e:
            print(f"Error saving calculation history: {e}")

    def record_calculation(self, expression: str, result, operation: str):
        """Saves a calculation to history and tracks it in the session."""
        now = datetime.now()
        entry = {
            "expression": expression,
            "result": result if isinstance(result, (int, float)) else str(result),
            "date": now.strftime("%Y-%m-%d"),
            "time": now.strftime("%H:%M:%S"),
            "operation": operation
        }
        self.history.append(entry)
        self.session_history.append(entry)
        self.save_data()

    # Memory Operations
    def memory_store(self, value: float):
        """Stores the given value in memory."""
        self.memory = float(value)

    def memory_recall(self) -> float:
        """Recalls the value stored in memory."""
        return self.memory

    def memory_clear(self):
        """Clears memory."""
        self.memory = 0.0

    # Basic/Core Operations
    def add(self, x: float, y: float) -> float:
        res = x + y
        self.record_calculation(f"{x} + {y}", res, "addition")
        return res

    def subtract(self, x: float, y: float) -> float:
        res = x - y
        self.record_calculation(f"{x} - {y}", res, "subtraction")
        return res

    def multiply(self, x: float, y: float) -> float:
        res = x * y
        self.record_calculation(f"{x} * {y}", res, "multiplication")
        return res

    def divide(self, x: float, y: float) -> float:
        if y == 0:
            raise ZeroDivisionError("Division by zero is undefined.")
        res = x / y
        self.record_calculation(f"{x} / {y}", res, "division")
        return res

    def modulus(self, x: float, y: float) -> float:
        if y == 0:
            raise ZeroDivisionError("Modulo by zero is undefined.")
        res = x % y
        self.record_calculation(f"{x} % {y}", res, "modulus")
        return res

    def power(self, x: float, y: float) -> float:
        if y > 10000:
            raise OverflowError("Exponent value is too high.")
        try:
            res = float(x ** y)
        except OverflowError as e:
            raise OverflowError("Calculation resulted in numerical overflow.") from e
        self.record_calculation(f"{x} ^ {y}", res, "power")
        return res

    # Scientific Operations
    def sqrt(self, x: float) -> float:
        if x < 0:
            raise ValueError("Cannot calculate the square root of a negative number.")
        res = math.sqrt(x)
        self.record_calculation(f"sqrt({x})", res, "square root")
        return res

    def factorial(self, x: float) -> int:
        if x < 0:
            raise ValueError("Cannot compute factorial of a negative number.")
        if not x.is_integer():
            raise ValueError("Factorial is only defined for integers.")
        
        val = int(x)
        if val > 1000:
            raise OverflowError("Value too large for standard factorial calculation.")
        res = math.factorial(val)
        self.record_calculation(f"factorial({val})", res, "factorial")
        return res

    def percentage(self, value: float, total: float) -> float:
        if total == 0:
            raise ZeroDivisionError("Total value cannot be zero for percentage.")
        res = (value / total) * 100.0
        self.record_calculation(f"{value} as % of {total}", res, "percentage")
        return res

    def absolute(self, x: float) -> float:
        res = abs(x)
        self.record_calculation(f"abs({x})", res, "absolute value")
        return res

    def log(self, x: float, base: float) -> float:
        if x <= 0:
            raise ValueError("Logarithm argument must be greater than zero.")
        if base <= 0 or base == 1:
            raise ValueError("Logarithm base must be greater than zero and not equal to 1.")
        res = math.log(x, base)
        self.record_calculation(f"log_{base}({x})", res, "logarithm")
        return res

    def ln(self, x: float) -> float:
        if x <= 0:
            raise ValueError("Natural logarithm argument must be greater than zero.")
        res = math.log(x)
        self.record_calculation(f"ln({x})", res, "natural log")
        return res

    def sin(self, x_deg: float) -> float:
        # Convert degree input to radians
        res = math.sin(math.radians(x_deg))
        self.record_calculation(f"sin({x_deg}°)", res, "sine")
        return res

    def cos(self, x_deg: float) -> float:
        res = math.cos(math.radians(x_deg))
        self.record_calculation(f"cos({x_deg}°)", res, "cosine")
        return res

    def tan(self, x_deg: float) -> float:
        # Tangent is undefined at odd multiples of 90 degrees
        if abs(x_deg % 180) == 90:
            raise ValueError("Tangent is undefined for odd multiples of 90 degrees.")
        res = math.tan(math.radians(x_deg))
        self.record_calculation(f"tan({x_deg}°)", res, "tangent")
        return res

    # Favorites Operations
    def add_to_favorites(self, index: int) -> bool:
        """Adds a calculation entry from the history to favorites by index."""
        if 0 <= index < len(self.history):
            entry = self.history[index]
            # Avoid duplicate favorites
            if entry not in self.favorites:
                self.favorites.append(entry)
                self.save_data()
                return True
        return False

    def remove_from_favorites(self, index: int) -> bool:
        """Removes a favorite entry by index."""
        if 0 <= index < len(self.favorites):
            self.favorites.pop(index)
            self.save_data()
            return True
        return False

    def clear_history(self):
        """Clears calculation history."""
        self.history = []
        self.save_data()

    def search_history(self, query: str) -> list:
        """Searches history for matching expressions, results, dates, or operations."""
        q = query.lower()
        results = []
        for entry in self.history:
            if (q in entry["expression"].lower() or 
                q in str(entry["result"]).lower() or 
                q in entry["operation"].lower() or
                q in entry["date"]):
                results.append(entry)
        return results

    # Precision
    def format_value(self, val) -> str:
        """Formats values according to decimal precision settings."""
        if isinstance(val, (int, float)):
            # If it's a whole number representing as float, make it cleaner
            if isinstance(val, float) and val.is_integer():
                return str(int(val))
            try:
                return f"{val:.{self.precision}f}".rstrip('0').rstrip('.') or '0'
            except ValueError:
                return str(val)
        return str(val)

    # Statistics & Reporting
    def get_statistics(self) -> dict:
        """Computes history statistics."""
        numeric_results = []
        op_counts = {}
        today_str = datetime.now().strftime("%Y-%m-%d")
        today_count = 0

        for entry in self.history:
            # Operation counts
            op = entry.get("operation", "unknown")
            op_counts[op] = op_counts.get(op, 0) + 1
            
            # Today's calculations count
            if entry.get("date") == today_str:
                today_count += 1
                
            # Parse result for stats if numeric
            try:
                res_val = float(entry["result"])
                numeric_results.append(res_val)
            except ValueError:
                pass

        total_calcs = len(self.history)
        most_used_op = max(op_counts, key=op_counts.get) if op_counts else "N/A"
        last_calc = self.history[-1] if self.history else None
        
        avg_res = sum(numeric_results) / len(numeric_results) if numeric_results else 0.0
        max_res = max(numeric_results) if numeric_results else 0.0
        min_res = min(numeric_results) if numeric_results else 0.0

        return {
            "total_calculations": total_calcs,
            "today_calculations": today_count,
            "most_used_operation": most_used_op,
            "last_calculation": last_calc,
            "average_result": avg_res,
            "largest_result": max_res,
            "smallest_result": min_res
        }

    def export_report(self, filename: str = "calculation_report.txt"):
        """Generates and writes a calculation report to a text file."""
        stats = self.get_statistics()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(filename, 'w', encoding='utf-8') as f:
            f.write("====================================================\n")
            f.write("      SCIENTIFIC CALCULATOR & UTILITIES REPORT      \n")
            f.write("====================================================\n")
            f.write(f"Generated on: {now}\n\n")

            f.write("-------------------- STATISTICS --------------------\n")
            f.write(f"Total Calculations (All-time): {stats['total_calculations']}\n")
            f.write(f"Today's Calculations         : {stats['today_calculations']}\n")
            f.write(f"Most Used Operation          : {stats['most_used_operation'].title()}\n")
            if stats['last_calculation']:
                last = stats['last_calculation']
                f.write(f"Last Calculation             : {last['expression']} = {last['result']}\n")
            else:
                f.write("Last Calculation             : N/A\n")
            f.write(f"Average Result               : {self.format_value(stats['average_result'])}\n")
            f.write(f"Largest Result               : {self.format_value(stats['largest_result'])}\n")
            f.write(f"Smallest Result              : {self.format_value(stats['smallest_result'])}\n\n")

            f.write("------------------- FAVORITES ---------------------\n")
            if self.favorites:
                for idx, entry in enumerate(self.favorites):
                    f.write(f"[{idx+1}] {entry['expression']} = {entry['result']}  ({entry['date']})\n")
            else:
                f.write("No favorite calculations saved yet.\n")
            f.write("\n")

            f.write("---------------- HISTORY LOG ----------------------\n")
            if self.history:
                for idx, entry in enumerate(self.history):
                    f.write(f"[{idx+1}] [{entry['date']} {entry['time']}] {entry['operation'].upper()}: {entry['expression']} = {entry['result']}\n")
            else:
                f.write("No calculations logged in history.\n")
            f.write("\n")
            f.write("====================================================\n")
            f.write("         End of Engineering Calculator Report       \n")
            f.write("====================================================\n")
