# Student Management System

A beginner-friendly, clean, command-line interface (CLI) application written in Python 3 to manage student records. This project demonstrates basic file handling (using CSV files), input validation, data presentation, and CRUD (Create, Read, Update, Delete) operations.

## Features
- **Add Student**: Add a new student record with Name, Roll Number, Course, Semester, and Marks.
- **View All Students**: Displays all records in a neat ASCII table, sorted by Roll Number, along with the total count.
- **Search Student**: Find a student's record by searching for their unique Roll Number.
- **Update Student**: Modify a student's details (Name, Roll Number, Course, Semester, and Marks). Press Enter during input to retain current values.
- **Delete Student**: Delete a student record with confirmation.
- **Persistent Storage**: Automatically saves all changes to a `students.csv` file and loads them on startup.

## Validation Rules
- **Roll Number**: Must be unique.
- **Semester**: Must be an integer between 1 and 8.
- **Marks**: Must be a number between 0 and 100.
- **Name and Course**: Cannot be blank/empty.

## How to Run
1. Make sure you have Python 3 installed.
2. Open a terminal/command prompt.
3. Navigate to the project directory:
   ```bash
   cd student-management-system
   ```
4. Run the application:
   ```bash
   python main.py
   ```

## Example Usage

### 1. Adding a Student
```text
=== Student Management System ===
1. Add Student
2. View All Students
3. Search Student
4. Update Student
5. Delete Student
6. Exit
Enter your choice (1-6): 1

--- Add Student ---
Enter Name: Divyansh Kumar
Enter Roll Number: BTECH/2026/001
Enter Course: B.Tech AI & Data Science
Enter Semester (1-8): 2
Enter Marks (0-100): 88.5
Success: Student added successfully!
```

### 2. Viewing All Students
All student records are printed sorted by Roll Number:
```text
+----------------+----------------+--------------------------+----------+-------+
| Name           | Roll Number    | Course                   | Semester | Marks |
+----------------+----------------+--------------------------+----------+-------+
| Divyansh Kumar | BTECH/2026/001 | B.Tech AI & Data Science | 2        | 88.5  |
| Rahul Verma    | BTECH/2026/002 | B.Tech CSE               | 4        | 79.0  |
| Priya Sharma   | BTECH/2026/003 | BCA                      | 1        | 92.0  |
| Ananya Singh   | BTECH/2026/004 | MCA                      | 3        | 85.0  |
+----------------+----------------+--------------------------+----------+-------+
Total Students: 4
```
