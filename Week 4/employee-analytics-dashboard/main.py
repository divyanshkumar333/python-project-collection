import sys
from utils import clear_screen, print_header, get_int_input, get_float_input, format_currency
from analyzer import EmployeeAnalyzer
from visualizer import EmployeeVisualizer
from report_generator import ReportGenerator

def display_dashboard(analyzer):
    clear_screen()
    print("=========================================")
    print("      Employee Analytics Dashboard       ")
    print("=========================================")
    if analyzer.is_loaded():
        stats = analyzer.get_summary_stats()
        print("Dataset Loaded Successfully")
        print(f"Total Employees:             {stats['Total Employees']}")
        print(f"Departments:                 {stats['Departments']}")
        print(f"Average Salary:              {format_currency(stats['Average Salary'])}")
        print(f"Average Experience:          {stats['Average Experience']:.1f} years")
        print(f"Average Performance Rating:  {stats['Average Performance Rating']:.1f}/5.0")
        print(f"Highest Salary:              {format_currency(stats['Highest Salary'])}")
        print(f"Lowest Salary:               {format_currency(stats['Lowest Salary'])}")
    else:
        print("Failed to load dataset. Please check data/employees.csv")
    print("=========================================\n")

def print_menu():
    print("Main Menu:")
    print("1. View Dataset Summary")
    print("2. Search Employee")
    print("3. Department Analytics")
    print("4. Salary Analytics")
    print("5. Experience Analytics")
    print("6. Performance Analytics")
    print("7. Filter Employees")
    print("8. Generate Charts")
    print("9. Export Filtered CSV")
    print("10. Generate Text Report")
    print("11. Export Dashboard Summary CSV")
    print("12. Exit")
    print("-" * 40)

def main():
    analyzer = EmployeeAnalyzer("data/employees.csv")
    visualizer = EmployeeVisualizer(analyzer.df)
    report_gen = ReportGenerator(analyzer)
    last_filtered_df = None
    
    display_dashboard(analyzer)
    
    while True:
        print_menu()
        choice = get_int_input("Enter your choice (1-12): ", 1, 12)
        
        if choice == 1:
            clear_screen()
            display_dashboard(analyzer)
            
        elif choice == 2:
            query = input("Enter Employee ID, Name, or Department to search: ")
            results = analyzer.search_employee(query)
            if results.empty:
                print("No employees found.")
            else:
                print(f"\nFound {len(results)} matches:")
                print(results.to_string(index=False))
                
        elif choice == 3:
            print_header("Department Analytics")
            dept_stats = analyzer.get_department_analytics()
            print(dept_stats.to_string(index=False))
            
        elif choice == 4:
            print_header("Salary Analytics")
            highest, lowest = analyzer.get_salary_analytics()
            print("--- Top 10 Highest Salaries ---")
            print(highest.to_string(index=False))
            print("\n--- Top 10 Lowest Salaries ---")
            print(lowest.to_string(index=False))
            
        elif choice == 5:
            print_header("Experience Analytics")
            exp_stats = analyzer.get_experience_analytics()
            for k, v in exp_stats.items():
                if isinstance(v, float):
                    print(f"{k}: {v:.1f} years")
                else:
                    print(f"{k}: {v}")
                    
        elif choice == 6:
            print_header("Performance Analytics")
            perf_stats = analyzer.get_performance_analytics()
            print(f"Average Rating: {perf_stats['Average Rating']:.1f}/5.0")
            print(f"Number of Highest Rated (5.0): {perf_stats['Highest Rated Count']}\n")
            print("--- Sample Highest Rated Employees ---")
            print(perf_stats['Highest Rated Samples'].to_string(index=False))
            print("\n--- Department-wise Average Rating ---")
            print(perf_stats['Department Ratings'].to_string(index=False))
            
        elif choice == 7:
            print_header("Filter Employees")
            dept = input("Enter Department (or press Enter to skip): ").strip()
            city = input("Enter City (or press Enter to skip): ").strip()
            
            min_sal = get_float_input("Enter Minimum Salary (or press Enter to skip): ", optional=True)
            max_sal = get_float_input("Enter Maximum Salary (or press Enter to skip): ", optional=True)
            min_exp = get_float_input("Enter Minimum Experience (or press Enter to skip): ", optional=True)
            min_rating = get_float_input("Enter Minimum Rating 1-5 (or press Enter to skip): ", optional=True)
            
            filtered = analyzer.filter_employees(
                department=dept if dept else None,
                city=city if city else None,
                min_salary=min_sal,
                max_salary=max_sal,
                min_exp=min_exp,
                min_rating=min_rating
            )
            
            if filtered.empty:
                print("No records found matching criteria.")
                last_filtered_df = None
            else:
                print(f"\nFound {len(filtered)} records:")
                print(filtered[["Employee ID", "Full Name", "Department", "Salary", "Experience (Years)", "Performance Rating"]].head(10).to_string(index=False))
                if len(filtered) > 10:
                    print(f"... and {len(filtered) - 10} more rows.")
                last_filtered_df = filtered
                
        elif choice == 8:
            print_header("Generating Charts")
            if visualizer.generate_all_charts():
                print("Charts generated successfully in the 'charts/' directory.")
                
        elif choice == 9:
            print_header("Export Filtered CSV")
            if last_filtered_df is None:
                print("No filtered data available. Please run 'Filter Employees' first.")
            else:
                filename = input("Enter filename (default: data/filtered_employees.csv): ").strip()
                if not filename:
                    filename = "data/filtered_employees.csv"
                if analyzer.export_filtered_data(last_filtered_df, filename):
                    print(f"Data successfully exported to {filename}.")
                    
        elif choice == 10:
            print_header("Generate Text Report")
            if report_gen.generate_text_report():
                print("Report successfully generated in 'reports/employee_summary_report.txt'.")
                
        elif choice == 11:
            print_header("Export Dashboard Summary CSV")
            if report_gen.export_summary_csv():
                print("Summary successfully exported to 'reports/dashboard_summary.csv'.")
                
        elif choice == 12:
            print("Exiting Employee Analytics Dashboard. Goodbye!")
            sys.exit(0)
            
        input("\nPress Enter to return to the main menu...")
        clear_screen()

if __name__ == "__main__":
    main()
