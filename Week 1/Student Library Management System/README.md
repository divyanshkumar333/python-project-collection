# Student Library Management System

A professional, clean, and beginner-friendly terminal-based Library Management System written in Python 3. This project demonstrates core Object-Oriented Programming (OOP) concepts, data persistence using JSON, proper input validation, and user-friendly CLI interaction using ANSI color codes.

## Features

1. **Display Available Books:** View a list of books that are currently available to borrow.
2. **Borrow Book:** Borrow a book using its title (case-insensitive). Availability checks prevent borrowing already checked-out books.
3. **Return Book:** Return a borrowed book, updating the library system automatically.
4. **Add New Book:** Add a new book to the library database. Prevents adding duplicate books.
5. **Search Book:** Fast, case-insensitive substring searching to easily locate books and see their status.
6. **View Borrowed Books:** See a tailored list of books borrowed by the currently logged-in student.
7. **Library Statistics:** View summary metrics of the library collection (Total books, Available, Borrowed, and number of Active Borrowers).
8. **Data Persistence:** Automatically saves and loads library data using a JSON file (`library.json`).

## OOP Design

This system leverages Object-Oriented Programming principles to separate concerns and ensure maintainable code:

- **Encapsulation:**
  - The `Library` class encapsulates all attributes and behaviors related to the book database (adding, search, borrowing, statistics, and persistence).
  - The `Student` class encapsulates student-specific details and query operations (e.g., extracting list of books borrowed by that specific student).
- **Single Responsibility Principle (SRP):**
  - `library.py` handles the data model, core operations, and state mutation.
  - `main.py` handles user interaction, user interface display, color printing, inputs, and validation.

## Folder Structure

```text
├── .gitignore          # Ignores pycache, local databases, and IDE configs
├── LICENSE             # MIT License
├── README.md           # Project documentation
├── library.json        # Persistent JSON database (auto-created on run)
├── library.py          # Core OOP classes (Library and Student)
├── main.py             # App CLI entry point and menu handler
└── requirements.txt    # Project dependencies description
```

## How to Run

### Prerequisites
- Python 3.x installed.

### Execution
Simply run the entrypoint file from your terminal:
```bash
python main.py
```

Upon launching, the program will prompt you for your name to log in, and then guide you through the interactive library menu.

## Future Improvements

- **Fine-Grained Permissions:** Implement multi-student login or an admin panel with passwords.
- **Due Dates and Fines:** Add borrow date tracking, due dates, and automated fine calculation for late returns.
- **Advanced Book Search:** Search by author name, genre, or publication year.
```
