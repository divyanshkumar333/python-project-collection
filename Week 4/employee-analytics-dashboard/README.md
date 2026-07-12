# Employee Analytics Dashboard

**Version 1.0.0**

## Project Overview
The Employee Analytics Dashboard is a professional, CLI-based Python application designed to analyze and visualize employee data. It serves as a comprehensive capstone project for a B.Tech Artificial Intelligence & Data Science portfolio. Using Python, Pandas, and Matplotlib, this project reads realistic Indian employee data, computes descriptive statistics, allows for complex filtering, and automatically generates visualizations and reports.

## Features
- **Data Loading & Validation:** Robust loading of CSV datasets, with graceful handling of missing values.
- **Search & Filtering:** Search employees by ID, Name, or Department. Filter by multiple criteria including Salary, Experience, City, and Performance Rating.
- **Comprehensive Analytics:** Breakdowns for Salary, Experience, Department, and Performance metrics.
- **Automated Reporting:** Generates text-based summary reports and exports dashboard metrics to CSV.
- **Data Visualization:** Uses Matplotlib to generate and save PNG charts for Salary Distributions, Department Headcounts, Experience Distributions, and Department Performance.
- **Modular Architecture:** Clean, Object-Oriented software design ensuring modularity and maintainability.

## Architecture
The application follows an Object-Oriented, modular architecture:
- **`utils.py`:** Provides pure helper functions for UI formatting and input validation.
- **`analyzer.py`:** Contains the `EmployeeAnalyzer` class. Encapsulates all Pandas DataFrame logic, including loading, filtering, and statistical aggregations.
- **`visualizer.py`:** Contains the `EmployeeVisualizer` class. Responsible for consuming data and generating Matplotlib plots.
- **`report_generator.py`:** Contains the `ReportGenerator` class. Formats the data into readable text summaries and dashboard CSV files.
- **`main.py`:** The entry point. Connects the user to the core modules through an interactive CLI.

## Folder Structure
```
employee-analytics-dashboard/
│
├── main.py
├── analyzer.py
├── visualizer.py
├── report_generator.py
├── utils.py
├── generate_data.py
│
├── data/
│   └── employees.csv
│
├── reports/
│   ├── employee_summary_report.txt
│   └── dashboard_summary.csv
│
├── charts/
│   ├── dept_count.png
│   ├── salary_dist.png
│   ├── top_10_salaries.png
│   ├── exp_dist.png
│   └── dept_performance.png
│
├── README.md
├── LICENSE
├── requirements.txt
└── .gitignore
```

## Technologies Used
- **Python 3.x**
- **Pandas** (Data analysis and manipulation)
- **Matplotlib** (Data visualization)

## Installation
1. Clone this repository or download the source code.
2. Ensure you have Python installed.
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. If you wish to regenerate the realistic dataset:
   ```bash
   python generate_data.py
   ```

## How to Run
To start the interactive dashboard:
```bash
python main.py
```
Follow the on-screen menu to navigate between different analytics views and reporting tools.

## Sample Outputs
*Placeholder: Insert screenshots of the CLI dashboard, generated charts, and report outputs here.*

## Future Improvements
- **GUI Integration:** Transition the CLI to a graphical user interface (GUI) using PyQt or a web dashboard using Streamlit/Dash.
- **Database Integration:** Connect the analyzer to a SQL database (e.g., PostgreSQL or SQLite) rather than static CSV files.
- **Advanced Machine Learning:** Implement predictive modeling to forecast employee attrition or salary trends.

## Learning Outcomes
Through building this project, the following skills were demonstrated:
- Proficiency in Python and Object-Oriented Programming (OOP).
- Advanced data manipulation and aggregation using Pandas.
- Data visualization best practices using Matplotlib.
- Modular software architecture and clean coding practices following PEP 8.
- CLI application design and robust error handling.

## Author
Developed by a motivated B.Tech Artificial Intelligence & Data Science student.
