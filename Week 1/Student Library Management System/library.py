"""
Module containing the core Student and Library classes for the Student Library Management System.
"""
import json
import os


class Student:
    """Represents a student using the library system."""

    def __init__(self, name: str):
        """
        Initialize a student object.

        Args:
            name (str): The name of the student.
        """
        self.name = name.strip()

    def get_borrowed_books(self, library_books: dict) -> list:
        """
        Retrieve list of books currently borrowed by this student.

        Args:
            library_books (dict): The dictionary of all books in the library.

        Returns:
            list: A list of book titles borrowed by the student.
        """
        return [
            title for title, info in library_books.items()
            if info.get("borrowed_by") == self.name
        ]


class Library:
    """Represents the library collection and operations."""

    def __init__(self, filepath: str = "library.json"):
        """
        Initialize the Library with a filepath for data persistence.

        Args:
            filepath (str): Path to the JSON file storing library data.
        """
        self.filepath = filepath
        self.books = {}
        self.load_books()

    def load_books(self):
        """Load books database from the JSON file. Fallback to empty if not found/corrupted."""
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    self.books = json.load(f)
            except json.JSONDecodeError:
                self.books = {}
        else:
            self.books = {}

    def save_books(self):
        """Save the current state of books to the JSON file."""
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(self.books, f, indent=4)
        except Exception as e:
            print(f"Error saving to database: {e}")

    def get_available_books(self) -> list:
        """
        Retrieve a list of books that are currently available.

        Returns:
            list: List of available book titles.
        """
        return [title for title, info in self.books.items() if info.get("borrowed_by") is None]

    def borrow_book(self, student: Student, book_title: str) -> tuple:
        """
        Borrow a book for a student.

        Args:
            student (Student): The student borrowing the book.
            book_title (str): The exact or matched title of the book.

        Returns:
            tuple: (bool, str) representing success status and descriptive message.
        """
        matched_title = self._find_exact_title(book_title)
        if not matched_title:
            return False, f"Book '{book_title}' does not exist in the library."

        book_info = self.books[matched_title]
        if book_info.get("borrowed_by") is not None:
            return False, f"Book '{matched_title}' is currently borrowed by {book_info['borrowed_by']}."

        self.books[matched_title]["borrowed_by"] = student.name
        self.save_books()
        return True, f"Successfully borrowed '{matched_title}'!"

    def return_book(self, student: Student, book_title: str) -> tuple:
        """
        Return a borrowed book.

        Args:
            student (Student): The student returning the book.
            book_title (str): The title of the book to return.

        Returns:
            tuple: (bool, str) representing success status and descriptive message.
        """
        matched_title = self._find_exact_title(book_title)
        if not matched_title:
            return False, f"Book '{book_title}' does not exist in the library."

        book_info = self.books[matched_title]
        if book_info.get("borrowed_by") != student.name:
            return False, f"You have not borrowed '{matched_title}'."

        self.books[matched_title]["borrowed_by"] = None
        self.save_books()
        return True, f"Successfully returned '{matched_title}'!"

    def add_book(self, book_title: str) -> tuple:
        """
        Add a new book to the library. Prevents duplicate titles (case-insensitive check).

        Args:
            book_title (str): Title of the new book.

        Returns:
            tuple: (bool, str) representing success status and descriptive message.
        """
        cleaned_title = book_title.strip()
        if not cleaned_title:
            return False, "Book title cannot be empty."

        matched_title = self._find_exact_title(cleaned_title)
        if matched_title:
            return False, f"Book '{matched_title}' already exists in the library."

        self.books[cleaned_title] = {"borrowed_by": None}
        self.save_books()
        return True, f"Successfully added '{cleaned_title}' to the library."

    def search_books(self, query: str) -> list:
        """
        Search books by title (case-insensitive substring match).

        Args:
            query (str): The search query.

        Returns:
            list: List of tuples (title, borrowed_by) matching the query.
        """
        query_lower = query.lower().strip()
        if not query_lower:
            return []
        results = []
        for title, info in self.books.items():
            if query_lower in title.lower():
                results.append((title, info.get("borrowed_by")))
        return results

    def get_statistics(self) -> dict:
        """
        Generate statistics about the library collection.

        Returns:
            dict: Collection statistics including total, borrowed, available, active_borrowers.
        """
        total_books = len(self.books)
        borrowed_books = sum(1 for info in self.books.values() if info.get("borrowed_by") is not None)
        available_books = total_books - borrowed_books
        active_borrowers = len({info["borrowed_by"] for info in self.books.values() if info.get("borrowed_by") is not None})
        
        return {
            "total_books": total_books,
            "borrowed_books": borrowed_books,
            "available_books": available_books,
            "active_borrowers": active_borrowers
        }

    def _find_exact_title(self, book_title: str) -> str:
        """
        Find the exact database key matching case-insensitively.

        Args:
            book_title (str): The title query.

        Returns:
            str: The exact key from the database, or empty string if not found.
        """
        target_lower = book_title.lower().strip()
        for title in self.books:
            if title.lower() == target_lower:
                return title
        return ""
