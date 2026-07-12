import matplotlib.pyplot as plt
import os

class EmployeeVisualizer:
    def __init__(self, df):
        self.df = df
        self.output_dir = "charts"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            
    def generate_all_charts(self):
        """Generates and saves all requested charts."""
        if self.df is None or self.df.empty:
            print("No data available to generate charts.")
            return False
            
        self.plot_employees_per_department()
        self.plot_salary_distribution()
        self.plot_top_10_salaries()
        self.plot_experience_distribution()
        self.plot_department_performance()
        return True
        
    def plot_employees_per_department(self):
        dept_counts = self.df["Department"].value_counts()
        plt.figure(figsize=(10, 6))
        dept_counts.plot(kind="bar", color='skyblue', edgecolor='black')
        plt.title("Employees per Department")
        plt.xlabel("Department")
        plt.ylabel("Number of Employees")
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, "dept_count.png"))
        plt.close()
        
    def plot_salary_distribution(self):
        plt.figure(figsize=(10, 6))
        plt.hist(self.df["Salary"], bins=15, edgecolor='black', color='lightgreen')
        plt.title("Salary Distribution")
        plt.xlabel("Salary (₹)")
        plt.ylabel("Frequency")
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, "salary_dist.png"))
        plt.close()
        
    def plot_top_10_salaries(self):
        top_10 = self.df.nlargest(10, "Salary")[["Full Name", "Salary"]]
        plt.figure(figsize=(10, 6))
        plt.barh(top_10["Full Name"], top_10["Salary"], color='coral', edgecolor='black')
        plt.title("Top 10 Salaries")
        plt.xlabel("Salary (₹)")
        plt.ylabel("Employee")
        plt.gca().invert_yaxis()  # Highest at top
        plt.grid(axis='x', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, "top_10_salaries.png"))
        plt.close()
        
    def plot_experience_distribution(self):
        plt.figure(figsize=(10, 6))
        plt.hist(self.df["Experience (Years)"], bins=10, edgecolor='black', color='mediumpurple')
        plt.title("Experience Distribution")
        plt.xlabel("Experience (Years)")
        plt.ylabel("Frequency")
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, "exp_dist.png"))
        plt.close()
        
    def plot_department_performance(self):
        dept_perf = self.df.groupby("Department")["Performance Rating"].mean()
        plt.figure(figsize=(10, 6))
        dept_perf.plot(kind="bar", color='gold', edgecolor='black')
        plt.title("Average Performance Rating per Department")
        plt.xlabel("Department")
        plt.ylabel("Average Rating (1-5)")
        plt.ylim(0, 5)
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, "dept_performance.png"))
        plt.close()
