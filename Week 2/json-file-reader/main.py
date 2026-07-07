import json
import os


def format_size(size_in_bytes):
    """Formats file size into human-readable format."""
    if size_in_bytes < 1024:
        return f"{size_in_bytes} Bytes"
    elif size_in_bytes < 1024 * 1024:
        return f"{size_in_bytes / 1024:.2f} KB"
    else:
        return f"{size_in_bytes / (1024 * 1024):.2f} MB"


def read_and_parse_json(filepath):
    """
    Reads a file path, checks for various errors, and parses the JSON.
    Returns a tuple: (parsed_data, error_message)
    """
    if not os.path.exists(filepath):
        return None, "Error: The file does not exist. Please check the path."

    if os.path.isdir(filepath):
        return None, "Error: The path points to a directory, not a file."

    try:
        # Check if the file is empty first
        file_size = os.path.getsize(filepath)
        if file_size == 0:
            return None, "Error: The file is empty."

        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data, None

    except PermissionError:
        return None, "Error: Permission denied. You do not have access to read this file."
    except json.JSONDecodeError as e:
        return None, f"Error: Invalid JSON syntax. {e.msg} on line {e.lineno}, column {e.colno}."
    except Exception as e:
        return None, f"Error: An unexpected error occurred: {str(e)}"


def display_json_info(filepath, data):
    """Displays information and statistics about the JSON file."""
    file_name = os.path.basename(filepath)
    file_size_bytes = os.path.getsize(filepath)
    formatted_size = format_size(file_size_bytes)

    # Determine type and element count
    if isinstance(data, dict):
        json_type = "Object"
        item_count = len(data)
        count_label = "Number of top-level keys"
    elif isinstance(data, list):
        json_type = "Array"
        item_count = len(data)
        count_label = "Number of top-level items"
    else:
        json_type = "Primitive (String/Number/Boolean/Null)"
        item_count = 1
        count_label = "Count"

    print("\n" + "=" * 50)
    print("                 FILE METADATA")
    print("=" * 50)
    print(f"File Name:      {file_name}")
    print(f"File Size:      {formatted_size}")
    print(f"JSON Type:      {json_type}")
    print(f"{count_label}: {item_count}")
    print("=" * 50)


def main():
    print("========================================")
    print("          JSON FILE READER CLI          ")
    print("========================================")
    print("Welcome! This tool helps you inspect and read JSON files.")

    while True:
        # Get file path from user
        user_input = input("\nEnter the path to a JSON file (or 'exit' to quit): ").strip()

        # Handle exit condition
        if user_input.lower() in ('exit', 'quit', 'q'):
            print("\nThank you for using JSON File Reader. Goodbye!")
            break

        # Remove surrounding quotes that might be added by drag-and-drop in some terminals
        filepath = user_input.strip("'\"")

        if not filepath:
            print("Please enter a valid path.")
            continue

        # Process and read the file
        data, error_msg = read_and_parse_json(filepath)

        if error_msg:
            print(error_msg)
            continue

        # Display basic metadata
        display_json_info(filepath, data)

        # Print formatted content
        print("\n--- JSON Contents ---")
        try:
            formatted_json = json.dumps(data, indent=4, ensure_ascii=False)
            print(formatted_json)
        except Exception as e:
            print(f"Error printing JSON: {e}")
        print("-" * 25)


if __name__ == "__main__":
    main()
