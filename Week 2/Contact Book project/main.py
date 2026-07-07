import json
import os

FILENAME = "contacts.json"

def load_contacts():
    """Load contacts from the JSON file. Handle missing or corrupted files."""
    if not os.path.exists(FILENAME):
        return {}
    
    try:
        with open(FILENAME, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print("\n[Warning] The contacts.json file is corrupted. Starting with an empty contact list.")
        return {}
    except IOError:
        print("\n[Error] Could not read contacts.json. Starting with an empty contact list.")
        return {}

def save_contacts(contacts):
    """Save contacts to the JSON file."""
    try:
        with open(FILENAME, "w") as file:
            json.dump(contacts, file, indent=4)
    except IOError:
        print("\n[Error] Could not save contacts to contacts.json.")

def validate_phone(phone):
    """Validate phone number using basic string methods."""
    # Remove common formatting characters: spaces, dashes, parentheses, plus sign
    cleaned = phone.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
    if cleaned.startswith("+"):
        cleaned = cleaned[1:]
    
    # Check if the remaining characters are digits and length is reasonable (7 to 15 digits)
    return cleaned.isdigit() and 7 <= len(cleaned) <= 15

def add_contact(contacts):
    """Add a new contact to the contact book."""
    print("\n--- Add Contact ---")
    name = input("Enter contact name: ").strip()
    if not name:
        print("Error: Name cannot be empty.")
        return

    # Check for duplicate names (case-insensitive)
    for existing_name in contacts:
        if existing_name.lower() == name.lower():
            print(f"Error: A contact with the name '{existing_name}' already exists.")
            return

    phone = input("Enter phone number: ").strip()
    if not validate_phone(phone):
        print("Error: Invalid phone number. (Must be 7-15 digits, digits and '+ - ( )' allowed).")
        return

    contacts[name] = phone
    save_contacts(contacts)
    print("\nContact added successfully.")

def view_all_contacts(contacts):
    """Display all contacts in the contact book."""
    print("\n--- All Contacts ---")
    if not contacts:
        print("No contacts found.")
        return

    # Find the longest name for formatting the output alignment
    max_name_len = max(len(name) for name in contacts)
    header_name = "Name"
    header_phone = "Phone Number"
    name_width = max(max_name_len, len(header_name))

    print(f"{header_name:<{name_width}} | {header_phone}")
    print("-" * (name_width + 3 + len(header_phone)))

    for name, phone in sorted(contacts.items()):
        print(f"{name:<{name_width}} | {phone}")

def search_contact(contacts):
    """Search for contacts by name (partial match)."""
    print("\n--- Search Contact ---")
    if not contacts:
        print("No contacts available to search.")
        return

    query = input("Enter name to search: ").strip().lower()
    if not query:
        print("Error: Search query cannot be empty.")
        return

    matches = []
    for name, phone in contacts.items():
        if query in name.lower():
            matches.append((name, phone))

    if not matches:
        print("No matching contacts found.")
        return

    contact_word = "contact" if len(matches) == 1 else "contacts"
    print(f"\nFound {len(matches)} {contact_word}:")
    for name, phone in matches:
        print(f"\n{name}\nPhone: {phone}")

def update_contact(contacts):
    """Update an existing contact's phone number."""
    print("\n--- Update Contact ---")
    if not contacts:
        print("No contacts available to update.")
        return

    name = input("Enter the name of the contact to update: ").strip()
    
    # Find matching name (case-insensitive check)
    target_name = None
    for existing_name in contacts:
        if existing_name.lower() == name.lower():
            target_name = existing_name
            break

    if not target_name:
        print(f"Error: Contact '{name}' not found.")
        return

    print(f"Current phone number for '{target_name}': {contacts[target_name]}")
    new_phone = input("Enter new phone number: ").strip()
    
    if not validate_phone(new_phone):
        print("Error: Invalid phone number.")
        return

    contacts[target_name] = new_phone
    save_contacts(contacts)
    print(f"Success: Contact '{target_name}' has been updated.")

def delete_contact(contacts):
    """Delete a contact from the contact book."""
    print("\n--- Delete Contact ---")
    if not contacts:
        print("No contacts available to delete.")
        return

    name = input("Enter the name of the contact to delete: ").strip()
    
    # Find matching name (case-insensitive check)
    target_name = None
    for existing_name in contacts:
        if existing_name.lower() == name.lower():
            target_name = existing_name
            break

    if not target_name:
        print(f"Error: Contact '{name}' not found.")
        return

    confirm = input(f"Are you sure you want to delete '{target_name}'? (y/n): ").strip().lower()
    if confirm == 'y' or confirm == 'yes':
        del contacts[target_name]
        save_contacts(contacts)
        print(f"Success: Contact '{target_name}' has been deleted.")
    else:
        print("Deletion canceled.")

def main():
    contacts = load_contacts()
    
    while True:
        print("\n===== CONTACT BOOK =====")
        print("1. Add Contact")
        print("2. View Contacts")
        print("3. Search Contact")
        print("4. Update Contact")
        print("5. Delete Contact")
        print("6. Exit")
        
        choice = input("Enter your choice: ").strip()
        
        if choice == "1":
            add_contact(contacts)
        elif choice == "2":
            view_all_contacts(contacts)
        elif choice == "3":
            search_contact(contacts)
        elif choice == "4":
            update_contact(contacts)
        elif choice == "5":
            delete_contact(contacts)
        elif choice == "6":
            print("\nExiting Contact Book. Goodbye!")
            break
        else:
            print("Error: Invalid choice. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    main()
