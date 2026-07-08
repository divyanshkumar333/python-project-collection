# Scientific Calculator & Engineering Toolkit (v1.0)

A modular, clean, and professional command-line Scientific Calculator and Engineering Toolkit built using Python. Designed with a B.Tech Artificial Intelligence & Data Science student portfolio aesthetic in mind, this project demonstrates strong object-oriented programming (OOP), file handling, secure input validation, dynamic formatting, and safe mathematical parsing.

---

## Folder Structure

```
scientific-calculator/
│
├── main.py                # Driver script (CLI implementation & session management)
├── calculator.py          # Core Calculator logic, historical statistics, reports & persistence
├── utils/                 # Sub-modules for modular utility division
│   ├── __init__.py        # Package initialization
│   ├── parser.py          # AST-based safe mathematical expression parser
│   ├── converters.py      # Unit converter & Number base system converter
│   ├── financial.py       # Financial formulas (Interest, Compound Interest, EMI)
│   └── engineering.py     # BMI & statistical analysis tools (Mean, Mode, Median, StdDev)
├── history.json           # JSON Database persisting user calculations & favorites
├── README.md              # Project documentation
├── LICENSE                # MIT License
└── requirements.txt       # Project dependencies (None - Standard Library only)
```

---

## Key Features

1. **Mathematical Calculators**:
   - **Standard Mode**: Arithmetic operations (`+`, `-`, `*`, `/`, `%`, `^`) with memory recalling capability.
   - **Safe Expression Mode**: Securely parses and evaluates multi-step formulas like `(25 + 5) * 8 - 10` using Python's `ast` module without resorting to unsafe `eval()`.
   - **Scientific Mode**: Computes Trigonometric (`sin`, `cos`, `tan` from degrees), Logarithmic (`log` with custom bases, natural log `ln`), factorials (`!`), square roots, percentages, and absolute values.
2. **Specialized Toolkits**:
   - **Financial Calculator**: Calculates Simple Interest (SI), Compound Interest (CI), Equated Monthly Installment (EMI), and percentage growth or decay.
   - **Engineering Stats**:
     - **BMI Calculator**: Uses weight (kg) and height (cm) to compute Body Mass Index with classification.
     - **Descriptive Statistics**: Analyzes arrays of numbers to calculate Mean, Median, Mode, Standard Deviation, and basic Averages utilizing Python's `statistics` module.
3. **Conversions**:
   - **Unit Converter**: Converts length (meter, kilometer, centimeter), weight (gram, kilogram), and temperature (Celsius, Fahrenheit, Kelvin).
   - **Number System Base Converter**: Converts numbers dynamically between Binary, Octal, Decimal, and Hexadecimal.
4. **References & Math Utilities**:
   - **Math Utilities**: Checks if integers are Prime, determines Even/Odd, and calculates GCD, LCM, or Fibonacci terms.
   - **Constants Sheet**: Quick access to values for Pi ($\pi$), Euler's number ($e$), Golden Ratio ($\phi$), and the Euler-Mascheroni constant ($\gamma$).
   - **Formula Reference**: Text-based reference cards for Geometry, Calculus, and Finance equations.
5. **Memory & Settings**:
   - Store ($M+$), recall ($MR$), and clear ($MC$) registers.
   - Custom **Decimal Precision Setting** (allows setting output rounding from 0 to 15 decimal places).
6. **History & Favorites**:
   - Full history log loaded and saved to `history.json`.
   - Ability to add, view, and remove favorites.
   - Outputs comprehensive lifetime and daily execution statistics.
7. **Reporting**:
   - Exports a detailed, structured audit log and statistical report to `calculation_report.txt`.

---

## OOP Design Principles Used

- **Encapsulation**: State such as decimal precision, active memory registers, session history, and loaded data are encapsulated within the `Calculator` class instance, exposed only through safe class interfaces.
- **Modularity**: Code is split cleanly across multiple modules. Main driver script handles CLI inputs, while core calculator operations, AST evaluation, statistics, and converters reside in distinct class libraries.
- **Robust Exception Handling**: Custom try-catch validation handles common computational edge cases including:
  - Division / modulo by zero
  - Undefined logarithms
  - Square roots of negative numbers
  - Decimal factorials
  - Number format input errors
  - Large power overflows

---

## Technologies Used

- **Language**: Python 3.8+
- **Standard Library Modules**:
  - `math`: For advanced trigonometry and logarithms.
  - `ast`: For parsing syntax trees safely.
  - `statistics`: For mean, median, mode, and standard deviation.
  - `json`: For persistence database structure.
  - `datetime`: For logging calculation times.
  - `sys`: For process exits.

---

## Installation & How to Run

### Prerequisites
- Python 3.8 or newer must be installed on your machine.

### Instructions

1. **Clone or copy the directory** to your local filesystem.
2. Navigate to the project root:
   ```bash
   cd scientific-calculator
   ```
3. Run the driver application:
   ```bash
   python main.py
   ```

---

## Example Usage

### Safe Expression Evaluation
```
Select main option: 1
Select math calculator: 2
Enter expression: (10 + 5) * 2 / e
Result: 11.0364
```

### Memory Interoperability
```
Select main option: 5
Select choice: 1
Enter value to store: 12.5

Select main option: 1
Select choice: 1
Enter first number: M
[RECALLED FROM MEMORY] 12.5
Enter operator: *
Enter second number: 2
Result: 25
```

---

## Future Improvements (V2.0 Ideas)

- **Variable Bindings**: Support assigning calculated values to temporary variables (e.g. `x = 25`, then evaluate `x * 2`).
- **Matrix Operations**: Add multidimensional matrix addition, multiplication, and determinants.
- **Graphing Utilities**: Display text-based graphing plots in the console for mathematical functions.
