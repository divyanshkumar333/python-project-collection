import pandas as pd
import os

class EmployeeAnalyzer:
    """Class to encapsulate all data analysis and Pandas DataFrame logic."""
    
    def __init__(self, data_path=os.path.join("data", "employees.csv")):
        self.data_path = data_path
        self.df = None
        self.load_data()
        
    def load_data(self):
        """Loads and validates the dataset, filling missing values gracefully."""
        try:
            self.df = pd.read_csv(self.data_path)
            if self.df.empty:
                return
                
            # Basic cleaning: fill NaNs if any
            self.df.fillna({
                "Salary": self.df["Salary"].mean() if not self.df["Salary"].isnull().all() else 0,
                "Experience (Years)": self.df["Experience (Years)"].mean() if not self.df["Experience (Years)"].isnull().all() else 0,
                "Performance Rating": 3
            }, inplace=True)
            self.df.dropna(subset=["Employee ID", "Full Name"], inplace=True)
        except (FileNotFoundError, pd.errors.EmptyDataError):
            self.df = pd.DataFrame()
            
    def is_loaded(self):
        """Checks if the dataframe is properly loaded and not empty."""
        return self.df is not None and not self.df.empty
        
    def get_summary_stats(self):
        """Returns basic summary statistics for the dashboard."""
        if not self.is_loaded():
            return None
            
        return {
            "Total Employees": len(self.df),
            "Departments": self.df["Department"].nunique(),
            "Average Salary": self.df["Salary"].mean(),
            "Highest Salary": self.df["Salary"].max(),
            "Lowest Salary": self.df["Salary"].min(),
            "Average Experience": self.df["Experience (Years)"].mean(),
            "Average Performance Rating": self.df["Performance Rating"].mean()
        }
        
    def search_employee(self, query):
        """Searches for employees matching the query in ID, Name, or Department."""
        if not self.is_loaded():
            return pd.DataFrame()
            
        q = str(query).lower()
        mask = (
            self.df["Employee ID"].str.lower().str.contains(q, na=False) |
            self.df["Full Name"].str.lower().str.contains(q, na=False) |
            self.df["Department"].str.lower().str.contains(q, na=False)
        )
        return self.df[mask]

    def get_department_analytics(self):
        """Returns analytics grouped by department."""
        if not self.is_loaded():
            return pd.DataFrame()
            
        return self.df.groupby("Department").agg(
            Employee_Count=("Employee ID", "count"),
            Average_Salary=("Salary", "mean"),
            Highest_Salary=("Salary", "max"),
            Lowest_Salary=("Salary", "min"),
            Avg_Performance=("Performance Rating", "mean")
        ).reset_index()
        
    def get_salary_analytics(self):
        """Returns top 10 highest and lowest salaries."""
        if not self.is_loaded():
            return None, None
            
        cols = ["Full Name", "Department", "Salary"]
        highest = self.df.nlargest(10, "Salary")[cols]
        lowest = self.df.nsmallest(10, "Salary")[cols]
        return highest, lowest
        
    def get_experience_analytics(self):
        """Returns analytics based on experience."""
        if not self.is_loaded():
            return None
            
        most_exp = self.df.nlargest(1, "Experience (Years)").iloc[0]
        least_exp = self.df.nsmallest(1, "Experience (Years)").iloc[0]
        
        return {
            "Average Experience": self.df["Experience (Years)"].mean(),
            "Most Experienced": f"{most_exp['Full Name']} ({most_exp['Experience (Years)']} yrs)",
            "Least Experienced": f"{least_exp['Full Name']} ({least_exp['Experience (Years)']} yrs)"
        }
        
    def get_performance_analytics(self):
        """Returns performance related analytics."""
        if not self.is_loaded():
            return None
            
        highest_rated = self.df[self.df["Performance Rating"] == self.df["Performance Rating"].max()]
        dept_rating = self.df.groupby("Department")["Performance Rating"].mean().reset_index()
        
        return {
            "Average Rating": self.df["Performance Rating"].mean(),
            "Highest Rated Count": len(highest_rated),
            "Highest Rated Samples": highest_rated[["Full Name", "Department", "Performance Rating"]].head(5),
            "Department Ratings": dept_rating
        }

    def filter_employees(self, department=None, min_salary=None, max_salary=None, min_exp=None, city=None, min_rating=None):
        """Filters the dataset based on multiple criteria."""
        if not self.is_loaded():
            return pd.DataFrame()
            
        filtered = self.df.copy()
        
        if department:
            filtered = filtered[filtered["Department"].str.lower() == department.lower()]
        if city:
            filtered = filtered[filtered["City"].str.lower() == city.lower()]
        if min_salary is not None:
            filtered = filtered[filtered["Salary"] >= min_salary]
        if max_salary is not None:
            filtered = filtered[filtered["Salary"] <= max_salary]
        if min_exp is not None:
            filtered = filtered[filtered["Experience (Years)"] >= min_exp]
        if min_rating is not None:
            filtered = filtered[filtered["Performance Rating"] >= min_rating]
            
        return filtered

    def export_filtered_data(self, df_filtered, filename=os.path.join("data", "filtered_employees.csv")):
        """Exports a filtered dataframe to CSV."""
        if df_filtered.empty:
            return False
        df_filtered.to_csv(filename, index=False)
        return True
