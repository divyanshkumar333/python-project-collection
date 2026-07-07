"""The Perfect Guess.

A professional, interactive command-line number guessing game.
Features difficulty levels, persistent high scores, statistics tracking,
and robust input validation.
"""

import json
import os
import random

# File paths
HISCORE_FILE = "hiscore.txt"
STATS_FILE = "stats.json"


def load_high_score() -> int | None:
    """Load the high score from hiscore.txt.

    Returns:
        int | None: The high score (fewest attempts to win) or None if no high
        score is set or the file is invalid.
    """
    if not os.path.exists(HISCORE_FILE):
        return None
    try:
        with open(HISCORE_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if content.isdigit():
                return int(content)
    except OSError:
        pass
    return None


def save_high_score(score: int) -> None:
    """Save the new high score to hiscore.txt.

    Args:
        score (int): The new high score.
    """
    try:
        with open(HISCORE_FILE, "w", encoding="utf-8") as f:
            f.write(str(score))
    except OSError as e:
        print(f"Error saving high score to file: {e}")


def load_stats() -> dict:
    """Load statistics from stats.json.

    Returns:
        dict: A dictionary containing games_played, games_won, and total_attempts.
    """
    default_stats = {
        "games_played": 0,
        "games_won": 0,
        "total_attempts": 0
    }
    if not os.path.exists(STATS_FILE):
        return default_stats
    try:
        with open(STATS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return default_stats


def save_stats(stats: dict) -> None:
    """Save statistics to stats.json.

    Args:
        stats (dict): The statistics dictionary to save.
    """
    try:
        with open(STATS_FILE, "w", encoding="utf-8") as f:
            json.dump(stats, f, indent=4)
    except OSError as e:
        print(f"Error saving statistics to file: {e}")


def reset_game_data() -> None:
    """Reset both high score and statistics files."""
    if os.path.exists(HISCORE_FILE):
        try:
            os.remove(HISCORE_FILE)
        except OSError as e:
            print(f"Error removing high score file: {e}")

    if os.path.exists(STATS_FILE):
        try:
            os.remove(STATS_FILE)
        except OSError as e:
            print(f"Error removing statistics file: {e}")
    print("\n[+] High score and statistics have been reset successfully!")


def display_rules() -> None:
    """Display the game rules and difficulty details."""
    rules = """
========================================
              GAME RULES
========================================
1. Choose a difficulty level:
   - Easy  : Guess a number between 1 and 50
   - Medium: Guess a number between 1 and 100
   - Hard  : Guess a number between 1 and 500
2. Enter your guess when prompted.
3. The game will give you feedback:
   - "Too High" if your guess is above the target.
   - "Too Low" if your guess is below the target.
4. Try to guess the number in as few attempts as possible!
5. You can type 'q' or 'quit' at any point during a game to forfeit.
========================================
"""
    print(rules)


def display_high_score_and_stats() -> None:
    """Display the best score and game statistics."""
    high_score = load_high_score()
    stats = load_stats()

    games_played = stats.get("games_played", 0)
    games_won = stats.get("games_won", 0)
    total_attempts = stats.get("total_attempts", 0)

    # Calculate average attempts for won games
    avg_attempts = (total_attempts / games_won) if games_won > 0 else 0.0

    best_score_str = str(high_score) if high_score is not None else "N/A"

    stats_display = f"""
========================================
        HIGH SCORE & STATISTICS
========================================
 Best Score (Fewest Attempts): {best_score_str}
 Games Played:                 {games_played}
 Games Won:                    {games_won}
 Average Attempts (per win):   {avg_attempts:.2f}
========================================
"""
    print(stats_display)


def choose_difficulty() -> tuple[str, int]:
    """Prompt the user to select a difficulty level.

    Returns:
        tuple[str, int]: A tuple containing the difficulty name (str) and
        the maximum target number (int).
    """
    print("\nSelect Difficulty Level:")
    print("1. Easy (1–50)")
    print("2. Medium (1–100)")
    print("3. Hard (1–500)")

    while True:
        choice = input("Enter choice (1-3): ").strip()
        if choice == "1":
            return "Easy", 50
        if choice == "2":
            return "Medium", 100
        if choice == "3":
            return "Hard", 500
        print("[-] Invalid selection. Please enter 1, 2, or 3.")


def play_game() -> None:
    """Run a single game session of 'The Perfect Guess'."""
    difficulty_name, max_val = choose_difficulty()
    target_number = random.randint(1, max_val)
    attempts = 0

    print(f"\n[+] Starting game on {difficulty_name} mode!")
    print(f"I have chosen a number between 1 and {max_val}. Good luck!")

    stats = load_stats()
    stats["games_played"] += 1
    save_stats(stats)

    while True:
        user_input = input(f"Guess the number (1-{max_val}) or 'q' to quit: ").strip()

        if user_input.lower() in ("q", "quit"):
            print(f"\n[-] You forfeited! The number was {target_number}.")
            break

        # Validate integer input
        try:
            guess = int(user_input)
        except ValueError:
            print("[-] Invalid input. Please enter a valid integer or 'q' to quit.")
            continue

        # Validate range
        if guess < 1 or guess > max_val:
            print(f"[-] Out of range. The number is between 1 and {max_val}.")
            continue

        attempts += 1

        if guess < target_number:
            print("Too Low")
        elif guess > target_number:
            print("Too High")
        else:
            # Correct guess
            print(f"\n🎉 CONGRATULATIONS! You guessed it in {attempts} attempts! 🎉")

            # Update stats
            stats = load_stats()
            stats["games_won"] += 1
            stats["total_attempts"] += attempts
            save_stats(stats)

            # Update high score
            current_high_score = load_high_score()
            if current_high_score is None or attempts < current_high_score:
                print(f"🏆 NEW HIGH SCORE! Previous: {current_high_score or 'None'} -> New: {attempts}")
                save_high_score(attempts)

            break


def main_menu() -> None:
    """Display the main menu and coordinate program execution."""
    while True:
        print("\n=== THE PERFECT GUESS ===")
        print("1. Play Game")
        print("2. View Rules")
        print("3. View High Score & Stats")
        print("4. Reset High Score & Stats")
        print("5. Exit")

        choice = input("Enter option (1-5): ").strip()

        if choice == "1":
            while True:
                play_game()
                replay = input("\nDo you want to play again? (y/n): ").strip().lower()
                if replay not in ("y", "yes"):
                    break
        elif choice == "2":
            display_rules()
        elif choice == "3":
            display_high_score_and_stats()
        elif choice == "4":
            confirm = input("Are you sure you want to reset all records? (y/n): ").strip().lower()
            if confirm in ("y", "yes"):
                reset_game_data()
        elif choice == "5":
            print("\nThank you for playing The Perfect Guess! Goodbye!")
            break
        else:
            print("[-] Invalid choice. Please select an option from 1 to 5.")


if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\n[-] Game terminated by user. Goodbye!")
