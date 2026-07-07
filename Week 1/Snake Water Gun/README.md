# Snake Water Gun Game

A feature-rich, interactive, and terminal-based Python implementation of the classic Indian game **"Snake, Water, Gun"** (similar to Rock-Paper-Scissors). This project is designed as a professional submission for an internship assignment, demonstrating modular programming, clean documentation, persistent data storage, and CLI aesthetics without third-party dependencies.

---

## 🎮 Game Rules

The game follows these simple mechanics:
*   🐍 **Snake** drinks 💧 **Water** (Snake wins)
*   💧 **Water** douses/rusts 🔫 **Gun** (Water wins)
*   🔫 **Gun** shoots/kills 🐍 **Snake** (Gun wins)
*   If both choices are the same, the round ends in a **Tie**.

---

## ✨ Features

-   **Styled CLI Interface:** Native styling using ANSI escape codes for colorful menus, scores, and text outputs.
-   **Interactive Numbered Menus:** Simple navigation between playing, viewing rules, checking all-time statistics, and exiting.
-   **Persistent Statistics:** Game records (Wins, Losses, Ties, Total sets, and Win percentages) are saved locally in a `stats.json` file.
-   **Multiple Game Modes:**
    -   *Single Round:* Quick casual match.
    -   *Best-of-5:* Competitive matches where the first to reach 3 points wins the set.
-   **Graceful User Input Handling:** Accepts single letters (e.g., `s`, `w`, `g`) or full words (e.g., `snake`, `water`, `gun`) case-insensitively, handling invalid options cleanly.
-   **Clean Code Standards:** Developed fully compliant with PEP 8 style guidelines with descriptive docstrings and comments.

---

## 📂 Project Structure

```
snake-water-gun/
├── .gitignore          # Rules for ignoring files in git (venv, cache, stats)
├── LICENSE             # MIT License
├── README.md           # Documentation (this file)
├── main.py             # Main entrypoint containing the game logic
└── requirements.txt    # Standard dependency file (currently empty)
```

---

## 🚀 Installation & How to Run

### Prerequisites
*   Python 3.x installed on your local machine.

### Getting Started

1.  **Clone this Repository** (or download the source directory):
    ```bash
    git clone https://github.com/yourusername/snake-water-gun.git
    cd snake-water-gun
    ```

2.  **Run the Game:**
    Since the application uses only Python's built-in standard library, you can execute it directly without any package installations:
    ```bash
    python main.py
    ```

---

## 📸 Screenshots / Gameplay Preview

Below are placeholders representing the terminal layout during gameplay:

### 1. Main Menu & ASCII Title
```text
  ____             _             __        __    _
 / ___| _ __   __ _| | _____      \ \      / /_ _| |_ ___ _ __
 \___ \| '_ \ / _` | |/ / _ \  ___  \ \ /\ / / _` | __/ _ \ '__|
  ___) | | | | (_| |   <  __/ |___|  \ V  V / (_| | |_  __/ |
 |____/|_| |_|\__,_|_|\_\___|         \_/\_/ \__,_|\__\___|_|

                  ____
                 / ___|_   _ _ __
                | |  _| | | | '_ \
                | |_| | |_| | | | |
                 \____|\__,_|_| |_|


Welcome to Snake-Water-Gun!

=== MAIN MENU ===
1. Play Game
2. View Rules
3. View Statistics
4. Exit
Enter choice (1-4):
```

### 2. Gameplay (Best of 5 Mode)
```text
Starting a Best-of-5 match!

[Score: Player 1 - 1 Computer (Ties: 0)]
Enter choice [Snake/Water/Gun] (or 'q' to quit current set): s

Your Choice: Snake
Computer's Choice: Water
You win this round!
----------------------------------------
```

---

## 🛠️ Future Improvements

-   [ ] **Difficulty Levels:** Implement smart AI choices instead of simple random selection (e.g., tracking player patterns).
-   [ ] **Graphical User Interface:** Build a lightweight desktop GUI using `tkinter`.
-   [ ] **Multiplayer Mode:** Introduce a local hot-seat or socket-based 2-player mode.
-   [ ] **Sound Effects:** Add sound cues for winning, losing, and tying rounds.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
