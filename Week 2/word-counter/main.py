import os

def get_file_size_kb(filepath):
    """Return the size of the file in Kilobytes, rounded to two decimal places."""
    try:
        size_bytes = os.path.getsize(filepath)
        return round(size_bytes / 1024, 2)
    except OSError:
        return 0.0

def clean_word(word):
    """Remove common punctuation from a word for cleaner length measurement."""
    # Keeps letters, numbers, and hyphens, stripping out dots, commas, quotes, etc.
    punctuation_to_remove = '.,!?;:"()[]{}*&^%$#@_+=/\\|<>`~'
    return word.strip(punctuation_to_remove)

def analyze_file(filepath):
    """Read the file and count lines, words, characters, and find the longest word."""
    # Check if the path points to a directory
    if os.path.isdir(filepath):
        raise IsADirectoryError("The path points to a directory, not a file.")

    # Check if the file is empty
    if os.path.getsize(filepath) == 0:
        raise ValueError("The selected file is empty.")

    line_count = 0
    word_count = 0
    char_count = 0
    longest_word = ""

    # Open with UTF-8 and handle decoding errors gracefully
    with open(filepath, 'r', encoding='utf-8') as file:
        for line in file:
            # We count characters including whitespaces and newlines
            char_count += len(line)

            # Strip leading/trailing whitespaces to check if the line is empty
            cleaned_line = line.strip()
            if not cleaned_line:
                continue

            # Increment line count for non-empty lines
            line_count += 1

            # Split line by whitespace to get words
            words = cleaned_line.split()
            word_count += len(words)

            # Track the longest word in the file
            for word in words:
                cleaned = clean_word(word)
                if len(cleaned) > len(longest_word):
                    longest_word = cleaned

    # Check if we read any characters or if the file was just whitespace/newlines
    if char_count == 0:
        raise ValueError("The file contains no readable characters.")

    return {
        "lines": line_count,
        "words": word_count,
        "chars": char_count,
        "longest_word": longest_word
    }

def display_statistics(filepath, size_kb, stats):
    """Display the analysis results to the user in a clean format."""
    filename = os.path.basename(filepath)
    
    print("\n" + "=" * 50)
    print(f" ANALYSIS RESULTS FOR: {filename}")
    print("=" * 50)
    print(f" File Name:      {filename}")
    print(f" File Path:      {filepath}")
    print(f" File Size:      {size_kb} KB")
    print(f" Total Lines:    {stats['lines']} (excluding empty lines)")
    print(f" Total Words:    {stats['words']}")
    print(f" Total Chars:    {stats['chars']} (including spaces/newlines)")
    
    if stats['longest_word']:
        longest_len = len(stats['longest_word'])
        print(f" Longest Word:   '{stats['longest_word']}' ({longest_len} chars)")
    else:
        print(" Longest Word:   N/A")
        
    print("=" * 50 + "\n")

def run_word_counter():
    """Main loop for the Word Counter command-line application."""
    print("Welcome to the Word Counter Application!")
    print("This program analyzes text (.txt) files and displays useful statistics.")
    
    while True:
        print("-" * 50)
        user_input = input("Enter the path to a text file (or 'q' to quit): ").strip()
        
        # Check if the user wants to quit
        if user_input.lower() == 'q':
            print("\nThank you for using Word Counter. Goodbye!")
            break
            
        if not user_input:
            print("Error: Input cannot be empty. Please enter a valid file path.")
            continue
            
        # Clean quotes if user dragged and dropped the file into the terminal
        filepath = user_input.strip('"\'')
        
        try:
            # Perform checks and run analysis
            size_kb = get_file_size_kb(filepath)
            results = analyze_file(filepath)
            display_statistics(filepath, size_kb, results)
            
        except FileNotFoundError:
            print(f"Error: The file '{filepath}' was not found. Please check the path.")
        except PermissionError:
            print(f"Error: Permission denied. You do not have access to read '{filepath}'.")
        except IsADirectoryError:
            print(f"Error: '{filepath}' is a directory. Please provide a path to a file.")
        except UnicodeDecodeError:
            print(f"Error: Could not decode '{filepath}'. Ensure it is a valid text file (UTF-8).")
        except ValueError as err:
            print(f"Error: {err}")
        except Exception as err:
            print(f"An unexpected error occurred: {err}")
            
        # Simple menu prompt to analyze another file or exit
        choice = input("Would you like to analyze another file? (y/n): ").strip().lower()
        if choice != 'y' and choice != 'yes':
            print("\nThank you for using Word Counter. Goodbye!")
            break

if __name__ == "__main__":
    run_word_counter()
