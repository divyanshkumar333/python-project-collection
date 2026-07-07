"""
Main entry point for the Student Library Management System.
Handles user inputs, displays the interactive menu, and performs validation.
"""
import sys
from library import Library, Student

# ANSI Color Codes for user-friendly terminal output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


def print_success(message: str):
    """Print a success message in green."""
    print(f"\n{GREEN}✔ {message}{RESET}")


def print_error(message: str):
    """Print an error message in red."""
    print(f"\n{RED}✘ Error: {message}{RESET}")


def print_info(message: str):
    """Print an informational message in cyan."""
    print(f"\n{CYAN}{message}{RESET}")


def display_menu():
    """Display the interactive command-line interface menu."""
    print(f"\n{BOLD}=== Student Library Management System ==={RESET}")
    print("1. Display Available Books")
    print("2. Borrow Book")
    print("3. Return Book")
    print("4. Add New Book")
    print("5. Search Book")
    print("6. View Borrowed Books")
    print("7. Library Statistics")
    print("8. Exit")
    print("=" * 41)


def get_validated_input(prompt: str, allow_empty: bool = False) -> str:
    """
    Prompt the user for input and validate it.

    Args:
        prompt (str): Prompt message to show to the user.
        allow_empty (bool): Whether empty inputs are allowed.

    Returns:
        str: Validated non-empty string (if allow_empty is False).
    """
    while True:
        try:
            user_input = input(prompt).strip()
            if not user_input and not allow_empty:
                print(f"{RED}Input cannot be empty. Please try again.{RESET}")
                continue
            return user_input
        except (KeyboardInterrupt, EOFError):
            print(f"\n{RED}Operation cancelled.{RESET}")
            sys.exit(0)


def main():
    """Main function containing CLI loop."""
    print_info("Welcome to the Student Library Management System")
    
    # Initialize the Library and load existing books
    library = Library("library.json")

    # Prompt for Student Name once at startup
    student_name = get_validated_input(f"{BOLD}Please enter your name to login: {RESET}")
    student = Student(student_name)
    print_success(f"Logged in as student: {student.name}")

    while True:
        display_menu()
        choice = get_validated_input(f"{BOLD}Enter your choice (1-8): {RESET}")

        if choice == '1':
            available = library.get_available_books()
            if not available:
                print_info("No books are currently available in the library.")
            else:
                print_info("Available Books in Library:")
                for idx, book in enumerate(available, 1):
                    print(f"  {idx}. {book}")

        elif choice == '2':
            book_title = get_validated_input("Enter the title of the book you want to borrow: ")
            success, msg = library.borrow_book(student, book_title)
            if success:
                print_success(msg)
            else:
                print_error(msg)

        elif choice == '3':
            book_title = get_validated_input("Enter the title of the book you want to return: ")
            success, msg = library.return_book(student, book_title)
            if success:
                print_success(msg)
            else:
                print_error(msg)

        elif choice == '4':
            book_title = get_validated_input("Enter the title of the book you want to add: ")
            success, msg = library.add_book(book_title)
            if success:
                print_success(msg)
            else:
                print_error(msg)

        elif choice == '5':
            query = get_validated_input("Enter search query (book title): ")
            results = library.search_books(query)
            if not results:
                print_info(f"No books found matching query: '{query}'")
            else:
                print_info(f"Search Results for '{query}':")
                for idx, (title, borrowed_by) in enumerate(results, 1):
                    status = f"{RED}[Borrowed by {borrowed_by}]{RESET}" if borrowed_by else f"{GREEN}[Available]{RESET}"
                    print(f"  {idx}. {title} - {status}")

        elif choice == '6':
            borrowed_books = student.get_borrowed_books(library.books)
            if not borrowed_books:
                print_info(f"You ({student.name}) have not borrowed any books.")
            else:
                print_info(f"Books borrowed by {student.name}:")
                for idx, book in enumerate(borrowed_books, 1):
                    print(f"  {idx}. {book}")

        elif choice == '7':
            stats = library.get_statistics()
            print_info("Library Statistics:")
            print(f"  • Total Books: {stats['total_books']}")
            print(f"  • Available Books: {stats['available_books']}")
            print(f"  • Borrowed Books: {stats['borrowed_books']}")
            print(f"  • Active Borrowers: {stats['active_borrowers']}")

        elif choice == '8':
            print_success("Thank you for using the Student Library Management System. Goodbye!")
            break

        else:
            print_error("Invalid choice. Please enter a number between 1 and 8.")


if __name__ == '__main__':
    main()
