import csv
import random
from datetime import datetime, timedelta

def generate_data():
    num_records = 200
    
    first_names_m = ["Aarav", "Vihaan", "Aditya", "Rohan", "Arjun", "Sai", "Krishna", "Ishaan", "Shaurya", "Atharv", "Rahul", "Amit", "Rohit", "Divyansh"]
    first_names_f = ["Ananya", "Diya", "Saanvi", "Aadya", "Priya", "Sneha", "Neha", "Kavya", "Isha", "Riya", "Aisha", "Mira", "Tara"]
    last_names = ["Sharma", "Verma", "Singh", "Patel", "Joshi", "Gupta", "Mishra", "Kumar", "Chauhan", "Bhat", "Reddy", "Nair"]
    
    cities = ["Gwalior", "Delhi", "Mumbai", "Bengaluru", "Hyderabad", "Pune", "Jaipur", "Indore", "Lucknow", "Chennai"]
    
    departments = [
        "AI & Data Science", "Software Development", "Data Analytics", 
        "Cyber Security", "Cloud Engineering", "DevOps", 
        "Human Resources", "Finance", "Marketing", "Operations"
    ]
    
    designations = {
        "AI & Data Science": ["Data Scientist", "AI Engineer", "ML Engineer"],
        "Software Development": ["Software Engineer", "Frontend Developer", "Backend Developer"],
        "Data Analytics": ["Data Analyst", "Business Analyst"],
        "Cyber Security": ["Security Analyst", "Penetration Tester"],
        "Cloud Engineering": ["Cloud Architect", "Cloud Engineer"],
        "DevOps": ["DevOps Engineer", "Site Reliability Engineer"],
        "Human Resources": ["HR Manager", "Recruiter"],
        "Finance": ["Financial Analyst", "Accountant"],
        "Marketing": ["Marketing Manager", "SEO Specialist"],
        "Operations": ["Operations Manager", "Supply Chain Analyst"]
    }
    
    with open("data/employees.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Employee ID", "Full Name", "Age", "Gender", "Department", "Designation", "City", "Salary", "Experience (Years)", "Joining Date", "Performance Rating"])
        
        for i in range(1, num_records + 1):
            emp_id = f"EMP{i:04d}"
            
            gender = random.choice(["Male", "Female"])
            if gender == "Male":
                first_name = random.choice(first_names_m)
            else:
                first_name = random.choice(first_names_f)
                
            last_name = random.choice(last_names)
            full_name = f"{first_name} {last_name}"
            
            age = random.randint(22, 60)
            department = random.choice(departments)
            designation = random.choice(designations[department])
            city = random.choice(cities)
            
            # Correlate salary, age, and experience somewhat reasonably
            experience = max(0, age - 22 - random.randint(0, 3)) 
            base_salary = 300000 + (experience * 50000)
            salary = random.randint(base_salary, base_salary + 200000)
            
            joining_date = datetime.now() - timedelta(days=random.randint(10, 365 * experience if experience > 0 else 365))
            joining_date_str = joining_date.strftime("%Y-%m-%d")
            
            rating = random.randint(1, 5)
            
            writer.writerow([emp_id, full_name, age, gender, department, designation, city, salary, experience, joining_date_str, rating])

if __name__ == "__main__":
    generate_data()
    print("Successfully generated data/employees.csv with 200 records.")
