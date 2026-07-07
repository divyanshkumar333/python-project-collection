# JSON File Reader

A simple, beginner-friendly Python 3 command-line application to read, format, and inspect JSON files. It displays key metadata about the file and handles potential file system or formatting errors gracefully.

This project is suitable for a beginner/intermediate Python portfolio.

## Features

- **Robust Error Handling**: Handles File Not Found, Permission Denied, Invalid JSON structure, and Empty Files.
- **File Metadata & Statistics**: Displays file name, file size, JSON type (Object/Array), and the count of top-level keys or items.
- **Beautiful Formatting**: Prints the JSON contents cleanly using consistent 4-space indentation.
- **Interactive CLI Loop**: Allows the user to read multiple files in sequence without restarting the application.
- **Zero Dependencies**: Uses only standard Python library modules.

## How to Run

1. Clone or download this project.
2. Open your terminal or command prompt in the project directory.
3. Run the application:
   ```bash
   python main.py
   ```

## Example Usage

### Reading a Valid File

```
========================================
          JSON FILE READER CLI          
========================================
Welcome! This tool helps you inspect and read JSON files.

Enter the path to a JSON file (or 'exit' to quit): sample.json

==================================================
                 FILE METADATA
==================================================
File Name:      sample.json
File Size:      338 Bytes
JSON Type:      Object
Number of top-level keys: 7
==================================================

--- JSON Contents ---
{
    "name": "Divyansh Kumar",
    "roll_number": "AIDS2026042",
    "course": "B.Tech AI & Data Science",
    "college": "MITS Gwalior",
    "semester": 4,
    "marks": {
        "Python": 92,
        "DBMS": 88,
        "Operating Systems": 90
    },
    "skills": [
        "Python",
        "Machine Learning",
        "SQL"
    ]
}
-------------------------
```

### Reading an Invalid File

```
Enter the path to a JSON file (or 'exit' to quit): invalid.json
Error: Invalid JSON syntax. Expecting property name enclosed in double quotes on line 3, column 3.
```
