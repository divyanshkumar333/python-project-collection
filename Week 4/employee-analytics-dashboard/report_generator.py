import os
import csv
from datetime import datetime
from utils import format_currency

class ReportGenerator:
    def __init__(self, analyzer):
        self.analyzer = analyzer
        self.output_dir = "reports"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            
    def generate_text_report(self):
        """Generates a text-based summary report."""
        if not self.analyzer.is_loaded():
            print("No data available to generate report.")
            return False
            
        stats = self.analyzer.get_summary_stats()
        dept_stats = self.analyzer.get_department_analytics()
        exp_stats = self.analyzer.get_experience_analytics()
        perf_stats = self.analyzer.get_performance_analytics()
        
        filename = os.path.join(self.output_dir, "employee_summary_report.txt")
        
        with open(filename, "w", encoding="utf-8") as f:
            report_content = f"""========================================
       EMPLOYEE ANALYTICS REPORT        
========================================

Generated On: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

--- Dataset Summary ---
Total Employees: {stats['Total Employees']}
Total Departments: {stats['Departments']}
Average Salary: {format_currency(stats['Average Salary'])}
Highest Salary: {format_currency(stats['Highest Salary'])}
Lowest Salary: {format_currency(stats['Lowest Salary'])}
Average Experience: {stats['Average Experience']:.1f} years
Average Performance Rating: {stats['Average Performance Rating']:.1f}/5.0

--- Experience Statistics ---
Most Experienced: {exp_stats['Most Experienced']}
Least Experienced: {exp_stats['Least Experienced']}

--- Performance Statistics ---
Employees with Highest Rating (5.0): {perf_stats['Highest Rated Count']}

--- Department Statistics ---
"""
            f.write(report_content)
            for _, row in dept_stats.iterrows():
                f.write(f"[{row['Department']}]\n")
                f.write(f"  Headcount: {row['Employee_Count']}\n")
                f.write(f"  Average Salary: {format_currency(row['Average_Salary'])}\n")
                f.write(f"  Average Rating: {row['Avg_Performance']:.1f}/5.0\n\n")
                
        return True

    def export_summary_csv(self):
        """Exports the dashboard summary as a CSV file."""
        if not self.analyzer.is_loaded():
            print("No data available to export.")
            return False
            
        stats = self.analyzer.get_summary_stats()
        filename = os.path.join(self.output_dir, "dashboard_summary.csv")
        
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Metric", "Value"])
            writer.writerow(["Total Employees", stats['Total Employees']])
            writer.writerow(["Total Departments", stats['Departments']])
            writer.writerow(["Average Salary", f"{stats['Average Salary']:.2f}"])
            writer.writerow(["Highest Salary", f"{stats['Highest Salary']:.2f}"])
            writer.writerow(["Lowest Salary", f"{stats['Lowest Salary']:.2f}"])
            writer.writerow(["Average Experience (Years)", f"{stats['Average Experience']:.1f}"])
            writer.writerow(["Average Performance Rating", f"{stats['Average Performance Rating']:.1f}"])
            
        return True
