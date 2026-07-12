import os

def clear_screen():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    """Prints a formatted header."""
    print("\n" + "=" * 40)
    print(f"{title.center(40)}")
    print("=" * 40 + "\n")

def get_int_input(prompt, min_val=None, max_val=None, optional=False):
    """Safely gets an integer input from the user."""
    while True:
        try:
            val_str = input(prompt).strip()
            if optional and not val_str:
                return None
            value = int(val_str)
            if min_val is not None and value < min_val:
                print(f"Please enter a value >= {min_val}.")
                continue
            if max_val is not None and value > max_val:
                print(f"Please enter a value <= {max_val}.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

def get_float_input(prompt, min_val=None, optional=False):
    """Safely gets a float input from the user."""
    while True:
        try:
            val_str = input(prompt).strip()
            if optional and not val_str:
                return None
            value = float(val_str)
            if min_val is not None and value < min_val:
                print(f"Please enter a value >= {min_val}.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def format_currency(value):
    """Formats a number as Indian Rupee currency."""
    return f"₹{value:,.2f}"
