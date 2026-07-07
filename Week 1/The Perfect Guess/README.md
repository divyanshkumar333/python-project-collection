# The Perfect Guess

A professional, feature-rich command-line number-guessing game implemented in Python 3. This project is designed for beginners and demonstrates best practices in Python development, including robust user-input validation, modular functions, file persistence, and comprehensive statistics tracking.

## Features

- **Three Difficulty Levels**:
  - **Easy**: Guess numbers between 1 and 50.
  - **Medium**: Guess numbers between 1 and 100.
  - **Hard**: Guess numbers between 1 and 500.
- **Persistent High Score**: Stores your overall fewest-attempts score in `hiscore.txt`. Beats and updates the score automatically when you play better.
- **Detailed Statistics**: Tracks games played, games won, average attempts, and best score in `stats.json`.
- **User-Friendly Interface**: Features an interactive main menu.
- **Robust Validation**: Gracefully handles non-integer inputs, out-of-bounds guesses, and unexpected keypresses.
- **Replay Ability**: Lets you play multiple games in a row without restarting the program.
- **Forfeit Option**: Allows you to exit a game session at any time by typing `q` or `quit`.

## Project Structure

```text
├── .gitignore          # Ignores byte-compiled Python files and user environment configs
├── LICENSE             # MIT License
├── README.md           # Project documentation and guide
├── main.py             # Main entry point containing game logic and menus
├── requirements.txt    # Standard dependencies list (none required)
├── hiscore.txt         # Stores the single integer high score
└── stats.json          # Stores the persistent statistics history
```

## How to Play

1. Clone or download the workspace files.
2. Open a terminal/command prompt in the project folder.
3. Run the game using the Python launcher:
   ```bash
   py main.py
   ```
   *(or `python main.py` / `python3 main.py` depending on your environment).*
4. Select option `1` to play a game, or option `2` to read the detailed rules.
5. In game, enter guesses and receive hints ("Too High" or "Too Low") until you find the perfect guess!
6. Select option `3` from the main menu at any time to view your Best Score and complete performance statistics.
7. Use option `4` to reset all scores and starting fresh.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
