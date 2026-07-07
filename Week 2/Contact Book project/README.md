# Contact Book

A simple command-line Contact Book application written in Python 3. It is designed to be lightweight, easy to understand, and operates directly in the terminal.

## Description
This project is a menu-driven CLI application that allows users to manage a collection of contacts. Each contact consists of a name and a phone number. The contacts are saved locally to a `contacts.json` file, ensuring that the data persists even after closing the program.

## Features
- **Add Contact**: Add new contacts with a name and a phone number.
- **View All Contacts**: View a formatted list of all saved contacts sorted alphabetically.
- **Search Contact**: Search for contacts using partial name matching (case-insensitive).
- **Update Contact**: Update the phone number of an existing contact.
- **Delete Contact**: Delete an existing contact with a confirmation prompt.
- **Data Persistence**: Contacts are automatically saved to and loaded from `contacts.json`.
- **Validation & Error Handling**:
  - Validates phone numbers (must be between 7 and 15 digits).
  - Prevents adding duplicate contact names (case-insensitive).
  - Gracefully handles missing or corrupted JSON database files.

## How to Run

### Prerequisites
Make sure you have Python 3 installed on your system. You can verify this by running:
```bash
python --version
```
*Note: If `python` is not recognized, try using `py --version` instead.*

### Running the Application
1. Open your terminal or command prompt.
2. Navigate to the project folder `contact-book/`:
   ```bash
   cd contact-book
   ```
3. Execute the script:
   ```bash
   python main.py
   ```
   *Note: If `python` is not recognized on Windows, use:*
   ```bash
   py main.py
   ```

## Example Usage

### Adding a Contact
```text
===== CONTACT BOOK =====

1. Add Contact
2. View Contacts
3. Search Contact
4. Update Contact
5. Delete Contact
6. Exit

Enter your choice: 1

Enter contact name: Priya Sharma
Enter phone number: 9876543210

Contact added successfully.
```

### Viewing All Contacts
```text
===== CONTACT BOOK =====

1. Add Contact
2. View Contacts
3. Search Contact
4. Update Contact
5. Delete Contact
6. Exit

Enter your choice: 2

--- All Contacts ---
Name         | Phone Number
---------------------------
Priya Sharma | 9876543210
```

### Searching a Contact
```text
===== CONTACT BOOK =====

1. Add Contact
2. View Contacts
3. Search Contact
4. Update Contact
5. Delete Contact
6. Exit

Enter your choice: 3

Enter name to search: Priya

Found 1 contact:

Priya Sharma
Phone: 9876543210
```
