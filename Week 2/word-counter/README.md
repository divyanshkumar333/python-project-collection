# Word Counter

A clean, user-friendly command-line application that analyzes text (`.txt`) files and displays detailed statistics, including the line, word, and character counts, as well as the longest word in the file. 

This project is built using Python 3 and features robust error handling and a simple interactive command loop, making it a perfect addition to an internship portfolio.

## Features

- **File Statistics**: 
  - File name and path.
  - File size (in Kilobytes).
  - Total number of lines (excluding empty lines).
  - Total number of words.
  - Total number of characters (including spaces and newlines).
  - The longest word found in the file (excluding common punctuation).
- **Graceful Error Handling**: Detects and reports common errors like file not found, permission issues, empty files, directories passed as files, and invalid formats.
- **Interactive Session**: Allows analyzing multiple files consecutively without restarting the application.
- **Minimal Dependencies**: Built entirely using the Python standard library.

## How to Run

### Prerequisites
- Python 3.x installed.

### Setup and Execution

1. Clone or navigate to the project directory:
   ```bash
   cd word-counter
   ```

2. Run the application:
   ```bash
   python main.py
   ```

## Example Usage

```text
Welcome to the Word Counter Application!
This program analyzes text (.txt) files and displays useful statistics.
--------------------------------------------------
Enter the path to a text file (or 'q' to quit): sample.txt

==================================================
 ANALYSIS RESULTS FOR: sample.txt
==================================================
 File Name:      sample.txt
 File Path:      sample.txt
 File Size:      0.6 KB
 Total Lines:    7 (excluding empty lines)
 Total Words:    91
 Total Chars:    617 (including spaces/newlines)
 Longest Word:   'productivity' (12 chars)
==================================================

Would you like to analyze another file? (y/n): n

Thank you for using Word Counter. Goodbye!
```
