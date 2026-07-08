import sys
from calculator import Calculator
from utils.parser import SafeParser
from utils.converters import UnitConverter, NumberSystemConverter
from utils.financial import FinancialCalculator
from utils.engineering import EngineeringUtilities
from utils.math_utils import MathUtilities

def get_float_input(prompt: str, calculator: Calculator = None) -> float:
    """Prompts the user for a float number. Allows 'M' to recall memory value."""
    while True:
        user_input = input(prompt).strip()
        if calculator and user_input.lower() == 'm':
            val = calculator.memory_recall()
            print(f"[RECALLED FROM MEMORY] {calculator.format_value(val)}")
            return val
        try:
            return float(user_input)
        except ValueError:
            print("Invalid input. Please enter a valid real number (or 'M' to use memory).")

def get_int_input(prompt: str) -> int:
    """Prompts the user for an integer."""
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

def get_list_input(prompt: str) -> list[float]:
    """Prompts user to enter a list of numbers separated by spaces or commas."""
    while True:
        raw = input(prompt).strip()
        if not raw:
            print("Input cannot be empty.")
            continue
        # Split by comma or space
        parts = raw.replace(',', ' ').split()
        try:
            return [float(p) for p in parts]
        except ValueError:
            print("One or more values were invalid numbers. Please try again.")

def main():
    calc = Calculator()
    print("==================================================")
    print("   SCIENTIFIC CALCULATOR & ENGINEERING TOOLKIT    ")
    print("                  Version 1.0                     ")
    print("==================================================")

    while True:
        print("\n--- MAIN MENU ---")
        print("1. Mathematical Calculators (Standard, Expression, Scientific)")
        print("2. Specialized Toolkits (Financial, Engineering Stats)")
        print("3. Conversions (Unit Converter, Number Base)")
        print("4. References & Math Utilities (Prime, Fibonacci, Constants)")
        print("5. Memory & Settings (Store, Recall, Decimal Precision)")
        print("6. History, Statistics & Export")
        print("7. Exit")
        
        choice = input("\nEnter choice (1-7): ").strip()
        
        if choice == '1':
            handle_math_calculators(calc)
        elif choice == '2':
            handle_specialized_toolkits(calc)
        elif choice == '3':
            handle_conversions(calc)
        elif choice == '4':
            handle_references(calc)
        elif choice == '5':
            handle_memory_settings(calc)
        elif choice == '6':
            handle_history_statistics(calc)
        elif choice == '7':
            # Session Summary on Exit
            print("\n================ SESSION SUMMARY ================")
            session_len = len(calc.session_history)
            print(f"Total calculations performed this session: {session_len}")
            if session_len > 0:
                print("\nCalculations list:")
                for idx, entry in enumerate(calc.session_history):
                    print(f"  {idx+1}. {entry['expression']} = {calc.format_value(entry['result'])}")
            print("=================================================")
            print("\nThank you for using the Scientific Calculator & Engineering Toolkit. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")

# --- Submenu Handlers ---

def handle_math_calculators(calc: Calculator):
    while True:
        print("\n--- MATHEMATICAL CALCULATORS ---")
        print("1. Standard Basic Calculator (+, -, *, /, %, ^)")
        print("2. Safe Expression Mode (Evaluate full math equations)")
        print("3. Scientific Functions (sin, cos, tan, log, ln, sqrt, factorial)")
        print("4. Back to Main Menu")
        
        choice = input("\nEnter choice (1-4): ").strip()
        if choice == '4':
            break
            
        try:
            if choice == '1':
                x = get_float_input("Enter first number: ", calc)
                op = input("Enter operator (+, -, *, /, %, ^): ").strip()
                y = get_float_input("Enter second number: ", calc)
                
                if op == '+':
                    res = calc.add(x, y)
                elif op == '-':
                    res = calc.subtract(x, y)
                elif op == '*':
                    res = calc.multiply(x, y)
                elif op == '/':
                    res = calc.divide(x, y)
                elif op == '%':
                    res = calc.modulus(x, y)
                elif op in ('^', '**'):
                    res = calc.power(x, y)
                else:
                    print("Unsupported operator.")
                    continue
                print(f"Result: {calc.format_value(res)}")
                
            elif choice == '2':
                print("Expression Mode allows standard variables 'pi' and 'e'.")
                expr = input("Enter mathematical expression (e.g. (25 + 5) * 8 - 10): ").strip()
                res = SafeParser.evaluate(expr)
                calc.record_calculation(expr, res, "expression")
                print(f"Result: {calc.format_value(res)}")
                
            elif choice == '3':
                print("\nScientific Functions:")
                print("1. Square Root (sqrt)")
                print("2. Factorial (!)")
                print("3. Percentage (Part/Total)")
                print("4. Absolute Value (abs)")
                print("5. Logarithm (log base x)")
                print("6. Natural Log (ln)")
                print("7. Trigonometric functions (Sine/Cosine/Tangent in degrees)")
                sc_choice = input("Enter choice (1-7): ").strip()
                
                if sc_choice == '1':
                    val = get_float_input("Enter number: ", calc)
                    print(f"Result: {calc.format_value(calc.sqrt(val))}")
                elif sc_choice == '2':
                    val = get_float_input("Enter integer: ", calc)
                    print(f"Result: {calc.factorial(val)}")
                elif sc_choice == '3':
                    part = get_float_input("Enter part value: ", calc)
                    total = get_float_input("Enter total value: ", calc)
                    print(f"Result: {calc.format_value(calc.percentage(part, total))}%")
                elif sc_choice == '4':
                    val = get_float_input("Enter number: ", calc)
                    print(f"Result: {calc.format_value(calc.absolute(val))}")
                elif sc_choice == '5':
                    val = get_float_input("Enter value: ", calc)
                    base = get_float_input("Enter log base (e.g. 10, 2): ", calc)
                    print(f"Result: {calc.format_value(calc.log(val, base))}")
                elif sc_choice == '6':
                    val = get_float_input("Enter value: ", calc)
                    print(f"Result: {calc.format_value(calc.ln(val))}")
                elif sc_choice == '7':
                    val = get_float_input("Enter angle in degrees: ", calc)
                    print(f"Sine  : {calc.format_value(calc.sin(val))}")
                    print(f"Cosine: {calc.format_value(calc.cos(val))}")
                    try:
                        print(f"Tangent: {calc.format_value(calc.tan(val))}")
                    except ValueError as te:
                        print(f"Tangent: Undefined ({te})")
                else:
                    print("Invalid scientific option.")
            else:
                print("Invalid choice.")
        except (ValueError, ZeroDivisionError, OverflowError) as e:
            print(f"Math Error: {e}")

def handle_specialized_toolkits(calc: Calculator):
    while True:
        print("\n--- SPECIALIZED TOOLKITS ---")
        print("1. Financial Calculator")
        print("2. Engineering Utilities & Statistics")
        print("3. Back to Main Menu")
        
        choice = input("\nEnter choice (1-3): ").strip()
        if choice == '3':
            break
            
        try:
            if choice == '1':
                print("\nFinancial Submenu:")
                print("1. Simple Interest")
                print("2. Compound Interest")
                print("3. Equated Monthly Installment (EMI)")
                print("4. Percentage Increase/Decrease")
                fin_choice = input("Enter choice (1-4): ").strip()
                
                if fin_choice == '1':
                    p = get_float_input("Enter Principal Amount: ", calc)
                    r = get_float_input("Enter Annual Interest Rate (%): ", calc)
                    t = get_float_input("Enter Time (in years): ", calc)
                    res = FinancialCalculator.simple_interest(p, r, t)
                    print(f"Interest Amount: {calc.format_value(res['interest'])}")
                    print(f"Total Repayable: {calc.format_value(res['total_amount'])}")
                elif fin_choice == '2':
                    p = get_float_input("Enter Principal Amount: ", calc)
                    r = get_float_input("Enter Annual Interest Rate (%): ", calc)
                    t = get_float_input("Enter Time (in years): ", calc)
                    n = get_int_input("Enter compounding frequency (times per year, e.g. 1 for annual, 12 for monthly): ")
                    res = FinancialCalculator.compound_interest(p, r, t, n)
                    print(f"Interest Accumulated: {calc.format_value(res['interest'])}")
                    print(f"Total Amount        : {calc.format_value(res['total_amount'])}")
                elif fin_choice == '3':
                    p = get_float_input("Enter Loan Principal: ", calc)
                    r = get_float_input("Enter Annual Interest Rate (%): ", calc)
                    y = get_float_input("Enter Loan Period (years): ", calc)
                    res = FinancialCalculator.emi_calculator(p, r, y)
                    print(f"Monthly EMI: {calc.format_value(res['monthly_emi'])}")
                    print(f"Total Interest Payable: {calc.format_value(res['total_interest'])}")
                    print(f"Total Payment Amount  : {calc.format_value(res['total_payment'])}")
                elif fin_choice == '4':
                    orig = get_float_input("Enter original value: ", calc)
                    new_val = get_float_input("Enter new value: ", calc)
                    res = FinancialCalculator.percentage_change(orig, new_val)
                    print(f"Percentage {res['type'].title()}: {calc.format_value(res['change_percentage'])}%")
                else:
                    print("Invalid choice.")
                    
            elif choice == '2':
                print("\nEngineering Submenu:")
                print("1. BMI (Body Mass Index) Calculator")
                print("2. Percentage Calculators")
                print("3. List Descriptive Statistics (Mean, Median, Mode, Std Dev)")
                eng_choice = input("Enter choice (1-3): ").strip()
                
                if eng_choice == '1':
                    w = get_float_input("Enter Weight (kg): ", calc)
                    h = get_float_input("Enter Height (cm): ", calc)
                    res = EngineeringUtilities.calculate_bmi(w, h)
                    print(f"BMI: {calc.format_value(res['bmi'])}")
                    print(f"Classification: {res['category']}")
                elif eng_choice == '2':
                    print("1. What is X% of Y?")
                    print("2. X is what percent of Y?")
                    p_sub = input("Select percentage mode (1-2): ").strip()
                    if p_sub == '1':
                        x = get_float_input("Enter percent X: ", calc)
                        y = get_float_input("Enter base value Y: ", calc)
                        res = EngineeringUtilities.percentage_of_value(x, y)
                        print(f"Result: {calc.format_value(res)}")
                    elif p_sub == '2':
                        x = get_float_input("Enter part X: ", calc)
                        y = get_float_input("Enter total Y: ", calc)
                        res = EngineeringUtilities.value_as_percentage(x, y)
                        print(f"Result: {calc.format_value(res)}%")
                elif eng_choice == '3':
                    nums = get_list_input("Enter numbers separated by spaces or commas: ")
                    res = EngineeringUtilities.calculate_list_statistics(nums)
                    print(f"Count             : {res['count']}")
                    print(f"Average (Arithmetic): {calc.format_value(res['average'])}")
                    print(f"Mean              : {calc.format_value(res['mean'])}")
                    print(f"Median            : {calc.format_value(res['median'])}")
                    print(f"Mode              : {res['mode'] if isinstance(res['mode'], str) else calc.format_value(res['mode'])}")
                    print(f"Standard Deviation: {calc.format_value(res['std_dev'])}")
                else:
                    print("Invalid choice.")
            else:
                print("Invalid choice.")
        except (ValueError, ZeroDivisionError, OverflowError) as e:
            print(f"Error: {e}")

def handle_conversions(calc: Calculator):
    while True:
        print("\n--- CONVERSIONS ---")
        print("1. Unit Converter (Length, Weight, Temp)")
        print("2. Number System Base Converter")
        print("3. Back to Main Menu")
        
        choice = input("\nEnter choice (1-3): ").strip()
        if choice == '3':
            break
            
        try:
            if choice == '1':
                print("\nUnit Conversion Categories:")
                print("1. Length (Meter, Kilometer, Centimeter)")
                print("2. Weight (Gram, Kilogram)")
                print("3. Temperature (Celsius, Fahrenheit, Kelvin)")
                uc_choice = input("Enter choice (1-3): ").strip()
                
                if uc_choice == '1':
                    val = get_float_input("Enter value: ", calc)
                    from_u = input("Convert from (meter, kilometer, centimeter): ").strip()
                    to_u = input("Convert to (meter, kilometer, centimeter): ").strip()
                    res = UnitConverter.convert_length(val, from_u, to_u)
                    print(f"Result: {calc.format_value(res)} {to_u}")
                elif uc_choice == '2':
                    val = get_float_input("Enter value: ", calc)
                    from_u = input("Convert from (gram, kilogram): ").strip()
                    to_u = input("Convert to (gram, kilogram): ").strip()
                    res = UnitConverter.convert_weight(val, from_u, to_u)
                    print(f"Result: {calc.format_value(res)} {to_u}")
                elif uc_choice == '3':
                    val = get_float_input("Enter temperature value: ", calc)
                    from_u = input("Convert from (Celsius/C, Fahrenheit/F, Kelvin/K): ").strip()
                    to_u = input("Convert to (Celsius/C, Fahrenheit/F, Kelvin/K): ").strip()
                    res = UnitConverter.convert_temperature(val, from_u, to_u)
                    print(f"Result: {calc.format_value(res)} {to_u.upper()}")
                else:
                    print("Invalid choice.")
                    
            elif choice == '2':
                val_str = input("Enter value (e.g. 1010, 255, FF): ").strip()
                print("Select input base: 2 (Bin), 8 (Oct), 10 (Dec), 16 (Hex)")
                b_from = get_int_input("Input Base: ")
                print("Select output base: 2 (Bin), 8 (Oct), 10 (Dec), 16 (Hex)")
                b_to = get_int_input("Output Base: ")
                
                dec = NumberSystemConverter.to_decimal(val_str, b_from)
                res = NumberSystemConverter.from_decimal(dec, b_to)
                print(f"Base-{b_from} value '{val_str}' to Base-{b_to} = {res}")
            else:
                print("Invalid choice.")
        except ValueError as e:
            print(f"Conversion Error: {e}")

def handle_references(calc: Calculator):
    while True:
        print("\n--- REFERENCES & MATH UTILITIES ---")
        print("1. Mathematical Utilities (Prime, GCD, LCM, Fibonacci)")
        print("2. View Mathematical Constants")
        print("3. View Formula Cheat Sheet")
        print("4. Back to Main Menu")
        
        choice = input("\nEnter choice (1-4): ").strip()
        if choice == '4':
            break
            
        try:
            if choice == '1':
                print("\nMath Utilities:")
                print("1. Prime Number Check")
                print("2. Even/Odd Check")
                print("3. Greatest Common Divisor (GCD)")
                print("4. Least Common Multiple (LCM)")
                print("5. Fibonacci Series Generator")
                mu_choice = input("Enter choice (1-5): ").strip()
                
                if mu_choice == '1':
                    val = get_int_input("Enter positive integer: ")
                    res = MathUtilities.is_prime(val)
                    print(f"Is {val} Prime? {'Yes' if res else 'No'}")
                elif mu_choice == '2':
                    val = get_int_input("Enter integer: ")
                    print(f"{val} is {MathUtilities.check_even_odd(val)}.")
                elif mu_choice == '3':
                    a = get_int_input("Enter first integer: ")
                    b = get_int_input("Enter second integer: ")
                    print(f"GCD({a}, {b}) = {MathUtilities.gcd(a, b)}")
                elif mu_choice == '4':
                    a = get_int_input("Enter first integer: ")
                    b = get_int_input("Enter second integer: ")
                    print(f"LCM({a}, {b}) = {MathUtilities.lcm(a, b)}")
                elif mu_choice == '5':
                    n = get_int_input("Enter number of Fibonacci terms to generate: ")
                    res = MathUtilities.generate_fibonacci(n)
                    print(f"Fibonacci Sequence ({n} terms): {res}")
                else:
                    print("Invalid choice.")
                    
            elif choice == '2':
                print("\n--- MATHEMATICAL CONSTANTS ---")
                for name, info in MathUtilities.CONSTANTS.items():
                    print(f"{name:<35} : {info[0]:.15f} | {info[1]}")
                    
            elif choice == '3':
                print("\n--- FORMULA REFERENCE CHEAT SHEET ---")
                for category, formulas in MathUtilities.FORMULAS.items():
                    print(f"\n[{category}]")
                    for form in formulas:
                        print(f"  • {form}")
            else:
                print("Invalid choice.")
        except ValueError as e:
            print(f"Error: {e}")

def handle_memory_settings(calc: Calculator):
    while True:
        print("\n--- MEMORY & SETTINGS ---")
        print(f"Current Precision: {calc.precision} decimal places")
        print(f"Current Memory value: {calc.format_value(calc.memory_recall())}")
        print("1. Memory Store (M+)")
        print("2. Memory Recall (MR)")
        print("3. Memory Clear (MC)")
        print("4. Change Decimal Precision")
        print("5. Back to Main Menu")
        
        choice = input("\nEnter choice (1-5): ").strip()
        if choice == '5':
            break
            
        if choice == '1':
            val = get_float_input("Enter number to store in memory: ", calc)
            calc.memory_store(val)
            print("Value stored in memory.")
        elif choice == '2':
            print(f"Memory Value: {calc.format_value(calc.memory_recall())}")
        elif choice == '3':
            calc.memory_clear()
            print("Memory cleared.")
        elif choice == '4':
            p = get_int_input("Enter decimal precision places (0-15): ")
            if 0 <= p <= 15:
                calc.precision = p
                print(f"Precision set to {p} decimal places.")
            else:
                print("Precision must be between 0 and 15.")
        else:
            print("Invalid choice.")

def handle_history_statistics(calc: Calculator):
    while True:
        print("\n--- HISTORY, STATISTICS & EXPORT ---")
        print("1. View Full Calculation History")
        print("2. Search Calculation History")
        print("3. Clear History")
        print("4. Manage Favorites (View, Add, Remove)")
        print("5. View Comprehensive Statistics")
        print("6. Export Report (calculation_report.txt)")
        print("7. Back to Main Menu")
        
        choice = input("\nEnter choice (1-7): ").strip()
        if choice == '7':
            break
            
        if choice == '1':
            print("\n--- CALCULATION HISTORY ---")
            if not calc.history:
                print("No history recorded yet.")
            else:
                for idx, entry in enumerate(calc.history):
                    print(f"[{idx}] [{entry['date']} {entry['time']}] {entry['expression']} = {calc.format_value(entry['result'])}  (Op: {entry['operation']})")
                    
        elif choice == '2':
            q = input("Enter search query (operation name, date, expression, or result): ").strip()
            results = calc.search_history(q)
            print(f"\nSearch results for '{q}':")
            if not results:
                print("No matching records found.")
            else:
                for idx, entry in enumerate(results):
                    print(f"[{entry['date']} {entry['time']}] {entry['expression']} = {calc.format_value(entry['result'])}  (Op: {entry['operation']})")
                    
        elif choice == '3':
            confirm = input("Are you sure you want to clear all history? (y/n): ").strip().lower()
            if confirm == 'y':
                calc.clear_history()
                print("History cleared.")
                
        elif choice == '4':
            print("\n--- FAVORITES MANAGEMENT ---")
            print("1. View Favorites")
            print("2. Add Calculation from History to Favorites")
            print("3. Remove Favorite")
            fav_choice = input("Enter choice (1-3): ").strip()
            
            if fav_choice == '1':
                if not calc.favorites:
                    print("No favorites saved.")
                else:
                    for idx, entry in enumerate(calc.favorites):
                        print(f"[{idx}] {entry['expression']} = {calc.format_value(entry['result'])}")
            elif fav_choice == '2':
                if not calc.history:
                    print("No calculations in history to favorite.")
                else:
                    # Show recent calculations first to help them select
                    for idx in range(max(0, len(calc.history)-10), len(calc.history)):
                        entry = calc.history[idx]
                        print(f"[{idx}] {entry['expression']} = {calc.format_value(entry['result'])}")
                    h_idx = get_int_input("Enter calculation index from above to favorite: ")
                    if calc.add_to_favorites(h_idx):
                        print("Added to favorites.")
                    else:
                        print("Invalid index or already favorited.")
            elif fav_choice == '3':
                if not calc.favorites:
                    print("No favorites to remove.")
                else:
                    for idx, entry in enumerate(calc.favorites):
                        print(f"[{idx}] {entry['expression']} = {calc.format_value(entry['result'])}")
                    f_idx = get_int_input("Enter favorite index to remove: ")
                    if calc.remove_from_favorites(f_idx):
                        print("Removed from favorites.")
                    else:
                        print("Invalid index.")
                        
        elif choice == '5':
            stats = calc.get_statistics()
            print("\n--- COMPREHENSIVE STATISTICS ---")
            print(f"Total Calculations performed (all-time): {stats['total_calculations']}")
            print(f"Calculations performed today           : {stats['today_calculations']}")
            print(f"Calculations in current session         : {len(calc.session_history)}")
            print(f"Most Used Operation                     : {stats['most_used_operation'].title()}")
            print(f"Average Numeric Result                  : {calc.format_value(stats['average_result'])}")
            print(f"Largest Numeric Result                  : {calc.format_value(stats['largest_result'])}")
            print(f"Smallest Numeric Result                 : {calc.format_value(stats['smallest_result'])}")
            if stats['last_calculation']:
                last = stats['last_calculation']
                print(f"Last Calculation                        : {last['expression']} = {calc.format_value(last['result'])}")
                
        elif choice == '6':
            calc.export_report()
            print("Report exported successfully to 'calculation_report.txt'.")
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram interrupted. Exiting...")
        sys.exit(0)
