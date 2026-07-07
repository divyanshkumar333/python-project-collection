import os
import csv

CSV_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "students.csv")


def load_students():
    """Loads student records from the CSV file."""
    students = []
    if not os.path.exists(CSV_FILE):
        # Create file with headers if it doesn't exist
        with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Roll Number", "Course", "Semester", "Marks"])
        return students

    with open(CSV_FILE, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Basic validation/cleanup of types
            try:
                row["Semester"] = int(row["Semester"])
                row["Marks"] = float(row["Marks"])
                students.append(row)
            except ValueError:
                # Skip corrupt/invalid lines in CSV
                continue
    return students


def save_students(students):
    """Saves the current student records to the CSV file."""
    with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as file:
        fieldnames = ["Name", "Roll Number", "Course", "Semester", "Marks"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for student in students:
            writer.writerow(student)


def is_valid_name(name):
    return len(name.strip()) > 0


def is_valid_roll(roll, students, exclude_roll=None):
    roll = roll.strip()
    if not roll:
        return False
    for s in students:
        if s["Roll Number"].lower() == roll.lower() and s["Roll Number"].lower() != (exclude_roll or "").lower():
            return False
    return True


def is_valid_course(course):
    return len(course.strip()) > 0


def is_valid_semester(sem_str):
    try:
        sem = int(sem_str)
        return 1 <= sem <= 8
    except ValueError:
        return False


def is_valid_marks(marks_str):
    try:
        marks = float(marks_str)
        return 0 <= marks <= 100
    except ValueError:
        return False


def display_table(students):
    """Displays student records in a neat ASCII table."""
    if not students:
        print("\nNo student records found.")
        return

    # Define column widths based on headers and data
    headers = ["Name", "Roll Number", "Course", "Semester", "Marks"]
    widths = {h: len(h) for h in headers}

    for s in students:
        widths["Name"] = max(widths["Name"], len(str(s["Name"])))
        widths["Roll Number"] = max(widths["Roll Number"], len(str(s["Roll Number"])))
        widths["Course"] = max(widths["Course"], len(str(s["Course"])))
        widths["Semester"] = max(widths["Semester"], len(str(s["Semester"])))
        widths["Marks"] = max(widths["Marks"], len(f"{s['Marks']:.1f}"))

    # Print separator line
    sep = "+" + "+".join("-" * (widths[h] + 2) for h in headers) + "+"
    print("\n" + sep)

    # Print header line
    header_str = "|"
    for h in headers:
        header_str += f" {h.ljust(widths[h])} |"
    print(header_str)
    print(sep)

    # Print data rows
    for s in students:
        name_part = str(s["Name"]).ljust(widths["Name"])
        roll_part = str(s["Roll Number"]).ljust(widths["Roll Number"])
        course_part = str(s["Course"]).ljust(widths["Course"])
        sem_part = str(s["Semester"]).ljust(widths["Semester"])
        marks_part = f"{s['Marks']:.1f}".ljust(widths["Marks"])
        print(f"| {name_part} | {roll_part} | {course_part} | {sem_part} | {marks_part} |")

    print(sep)
    print(f"Total Students: {len(students)}")


def add_student(students):
    print("\n--- Add Student ---")
    
    name = input("Enter Name: ").strip()
    if not is_valid_name(name):
        print("Error: Name cannot be empty.")
        return

    roll = input("Enter Roll Number: ").strip()
    if not is_valid_roll(roll, students):
        print("Error: Roll Number must be unique and non-empty.")
        return

    course = input("Enter Course: ").strip()
    if not is_valid_course(course):
        print("Error: Course cannot be empty.")
        return

    sem_input = input("Enter Semester (1-8): ").strip()
    if not is_valid_semester(sem_input):
        print("Error: Semester must be an integer between 1 and 8.")
        return
    semester = int(sem_input)

    marks_input = input("Enter Marks (0-100): ").strip()
    if not is_valid_marks(marks_input):
        print("Error: Marks must be a number between 0 and 100.")
        return
    marks = float(marks_input)

    new_student = {
        "Name": name,
        "Roll Number": roll,
        "Course": course,
        "Semester": semester,
        "Marks": marks
    }
    students.append(new_student)
    save_students(students)
    print("Success: Student added successfully!")


def view_all_students(students):
    print("\n--- View All Students ---")
    # Sort students by Roll Number (alphanumeric sorting)
    sorted_students = sorted(students, key=lambda x: x["Roll Number"].lower())
    display_table(sorted_students)


def search_student(students):
    print("\n--- Search Student ---")
    roll = input("Enter Roll Number to search: ").strip()
    if not roll:
        print("Error: Roll Number cannot be empty.")
        return

    found = [s for s in students if s["Roll Number"].lower() == roll.lower()]
    if found:
        display_table(found)
    else:
        print("Error: Student with this Roll Number not found.")


def update_student(students):
    print("\n--- Update Student ---")
    roll = input("Enter Roll Number to update: ").strip()
    if not roll:
        print("Error: Roll Number cannot be empty.")
        return

    student = None
    for s in students:
        if s["Roll Number"].lower() == roll.lower():
            student = s
            break

    if not student:
        print("Error: Student not found.")
        return

    print("Note: Press Enter to keep the existing value.")

    name = input(f"Enter Name [{student['Name']}]: ").strip()
    if name:
        student["Name"] = name

    new_roll = input(f"Enter Roll Number [{student['Roll Number']}]: ").strip()
    if new_roll:
        if not is_valid_roll(new_roll, students, exclude_roll=student["Roll Number"]):
            print("Error: Roll Number must be unique and non-empty. Update aborted.")
            return
        student["Roll Number"] = new_roll

    course = input(f"Enter Course [{student['Course']}]: ").strip()
    if course:
        student["Course"] = course

    sem_input = input(f"Enter Semester [{student['Semester']}]: ").strip()
    if sem_input:
        if not is_valid_semester(sem_input):
            print("Error: Semester must be between 1 and 8. Update aborted.")
            return
        student["Semester"] = int(sem_input)

    marks_input = input(f"Enter Marks [{student['Marks']}]: ").strip()
    if marks_input:
        if not is_valid_marks(marks_input):
            print("Error: Marks must be between 0 and 100. Update aborted.")
            return
        student["Marks"] = float(marks_input)

    save_students(students)
    print("Success: Student record updated successfully!")


def delete_student(students):
    print("\n--- Delete Student ---")
    roll = input("Enter Roll Number to delete: ").strip()
    if not roll:
        print("Error: Roll Number cannot be empty.")
        return

    student = None
    for s in students:
        if s["Roll Number"].lower() == roll.lower():
            student = s
            break

    if not student:
        print("Error: Student not found.")
        return

    confirm = input(f"Are you sure you want to delete student '{student['Name']}'? (yes/no): ").strip().lower()
    if confirm in ["yes", "y"]:
        students.remove(student)
        save_students(students)
        print("Success: Student deleted successfully!")
    else:
        print("Operation cancelled. Student was not deleted.")


def main():
    students = load_students()
    while True:
        print("\n=== Student Management System ===")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Exit")
        
        choice = input("Enter your choice (1-6): ").strip()
        if choice == "1":
            add_student(students)
        elif choice == "2":
            view_all_students(students)
        elif choice == "3":
            search_student(students)
        elif choice == "4":
            update_student(students)
        elif choice == "5":
            delete_student(students)
        elif choice == "6":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Error: Invalid choice. Please enter a number between 1 and 6.")


if __name__ == "__main__":
    main()
