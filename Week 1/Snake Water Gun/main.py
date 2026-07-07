"""
Snake Water Gun Game - A Python implementation of the classic game.

Rules:
- Snake vs Water: Snake drinks Water (Snake wins)
- Water vs Gun: Water douses Gun (Water wins)
- Gun vs Snake: Gun kills Snake (Gun wins)
- Same choices result in a Tie.

This game supports persistent statistics storage, custom game modes (Single
Round or Best-of-5), and a styled CLI interface using ANSI colors.
"""

import json
import os
import random

# ANSI Escape Codes for CLI Styling
COLOR_RESET = "\033[0m"
COLOR_BOLD = "\033[1m"
COLOR_RED = "\033[91m"
COLOR_GREEN = "\033[92m"
COLOR_YELLOW = "\033[93m"
COLOR_BLUE = "\033[94m"
COLOR_MAGENTA = "\033[95m"
COLOR_CYAN = "\033[96m"

STATS_FILE = "stats.json"

# ASCII Art Title
ASCII_ART = f"""
{COLOR_GREEN}  ____             _             __        __    _
 / ___| _ __   __ _| | _____      \\ \\      / /_ _| |_ ___ _ __
 \\___ \\| '_ \\ / _` | |/ / _ \\  ___  \\ \\ /\\ / / _` | __/ _ \\ '__|
  ___) | | | | (_| |   <  __/ |___|  \\ V  V / (_| | |_  __/ |
 |____/|_| |_|\\__,_|_|\\_\\___|         \\_/\\_/ \\__,_|\\__\\___|_|

                  ____
                 / ___|_   _ _ __
                | |  _| | | | '_ \\
                | |_| | |_| | | | |
                 \\____|\\__,_|_| |_|
{COLOR_RESET}
"""

GAME_RULES = f"""
{COLOR_BOLD}{COLOR_CYAN}--- Game Rules ---{COLOR_RESET}
1. {COLOR_GREEN}Snake{COLOR_RESET} vs {COLOR_BLUE}Water{COLOR_RESET} : {COLOR_GREEN}Snake{COLOR_RESET} wins (Snake drinks Water)
2. {COLOR_BLUE}Water{COLOR_RESET} vs {COLOR_RED}Gun{COLOR_RESET}   : {COLOR_BLUE}Water{COLOR_RESET} wins (Water douses/rusts Gun)
3. {COLOR_RED}Gun{COLOR_RESET}   vs {COLOR_GREEN}Snake{COLOR_RESET} : {COLOR_RED}Gun{COLOR_RESET} wins (Gun shoots Snake)
4. Same choices result in a {COLOR_YELLOW}Tie{COLOR_RESET}.
"""

# Map short codes or inputs to full names
CHOICES_MAP = {
    "s": "Snake",
    "w": "Water",
    "g": "Gun",
    "snake": "Snake",
    "water": "Water",
    "gun": "Gun"
}


def load_stats():
    """
    Load game statistics from a JSON file.

    Returns:
        dict: A dictionary containing absolute counts for wins, losses, ties,
              and total completed game sets.
    """
    default_stats = {
        "wins": 0,
        "losses": 0,
        "ties": 0,
        "total_sets": 0
    }
    if os.path.exists(STATS_FILE):
        try:
            with open(STATS_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            # If the file is corrupted or unreadable, fall back to defaults
            return default_stats
    return default_stats


def save_stats(stats):
    """
    Save the game statistics to a JSON file.

    Args:
        stats (dict): The dictionary containing current statistics.
    """
    try:
        with open(STATS_FILE, "w") as f:
            json.dump(stats, f, indent=4)
    except IOError as e:
        print(f"{COLOR_RED}Error saving statistics: {e}{COLOR_RESET}")


def get_computer_choice():
    """
    Randomly select the computer's choice.

    Returns:
        str: 'Snake', 'Water', or 'Gun'.
    """
    return random.choice(["Snake", "Water", "Gun"])


def get_user_choice():
    """
    Ask the user for their move choice and validate it.

    Allows shorthand letters ('s', 'w', 'g') or full words.
    Also handles requests to return to the menu or quit.

    Returns:
        str: The validated choice ('Snake', 'Water', or 'Gun'), or None if user wants to cancel.
    """
    while True:
        try:
            prompt = (
                f"Enter choice [{COLOR_GREEN}S{COLOR_RESET}nake/"
                f"{COLOR_BLUE}W{COLOR_RESET}ater/"
                f"{COLOR_RED}G{COLOR_RESET}un] (or 'q' to quit current set): "
            )
            user_input = input(prompt).strip().lower()
            if user_input == 'q':
                return None
            if user_input in CHOICES_MAP:
                return CHOICES_MAP[user_input]
            print(f"{COLOR_YELLOW}Invalid choice! Please choose Snake, Water, or Gun.{COLOR_RESET}")
        except (KeyboardInterrupt, EOFError):
            print("\n")
            return None


def determine_winner(player, computer):
    """
    Determine the winner of a single round.

    Args:
        player (str): The player's choice ('Snake', 'Water', 'Gun').
        computer (str): The computer's choice ('Snake', 'Water', 'Gun').

    Returns:
        str: 'player' if the player wins, 'computer' if the computer wins, or 'tie'.
    """
    if player == computer:
        return "tie"

    # Winning conditions for the player
    winning_combos = {
        ("Snake", "Water"),
        ("Water", "Gun"),
        ("Gun", "Snake")
    }

    if (player, computer) in winning_combos:
        return "player"
    return "computer"


def print_round_result(player, computer, result):
    """
    Print the outcome of a single round with styling.

    Args:
        player (str): The player's choice.
        computer (str): The computer's choice.
        result (str): The winner ('player', 'computer', or 'tie').
    """
    print(f"\nYour Choice: {COLOR_BOLD}{player}{COLOR_RESET}")
    print(f"Computer's Choice: {COLOR_BOLD}{computer}{COLOR_RESET}")

    if result == "player":
        print(f"{COLOR_GREEN}{COLOR_BOLD}You win this round!{COLOR_RESET}")
    elif result == "computer":
        print(f"{COLOR_RED}{COLOR_BOLD}Computer wins this round!{COLOR_RESET}")
    else:
        print(f"{COLOR_YELLOW}{COLOR_BOLD}It's a tie!{COLOR_RESET}")
    print("-" * 40)


def display_stats(stats):
    """
    Display persistent scoreboard and match statistics.

    Args:
        stats (dict): The loaded stats dict.
    """
    total = stats["wins"] + stats["losses"] + stats["ties"]
    win_percentage = (stats["wins"] / total * 100) if total > 0 else 0.0

    print(f"\n{COLOR_BOLD}{COLOR_MAGENTA}=== PERSISTENT ALL-TIME STATISTICS ==={COLOR_RESET}")
    print(f"Total Game Sets Finished: {stats['total_sets']}")
    print(f"Total Rounds Played:     {total}")
    print(f"Wins:                    {COLOR_GREEN}{stats['wins']}{COLOR_RESET}")
    print(f"Losses:                  {COLOR_RED}{stats['losses']}{COLOR_RESET}")
    print(f"Ties:                    {COLOR_YELLOW}{stats['ties']}{COLOR_RESET}")
    print(f"Win Percentage:          {win_percentage:.2f}%")
    print(f"{COLOR_MAGENTA}====================================={COLOR_RESET}\n")


def play_game_loop(stats):
    """
    Run the play loop which allows choosing between Single Round and Best-of-5.

    Updates and saves the persistent statistics object.

    Args:
        stats (dict): The mutable stats dict.
    """
    while True:
        print(f"\n{COLOR_BOLD}{COLOR_CYAN}--- Game Settings ---{COLOR_RESET}")
        print("1. Single Round Match")
        print("2. Best-of-5 Match")
        print("3. Back to Main Menu")

        choice = input("Select game mode (1-3): ").strip()
        if choice == '3':
            break
        if choice not in ('1', '2'):
            print(f"{COLOR_YELLOW}Please select a valid option (1-3).{COLOR_RESET}")
            continue

        target_wins = 1 if choice == '1' else 3
        game_mode_name = "Single Round" if target_wins == 1 else "Best-of-5"

        print(f"\nStarting a {COLOR_BOLD}{COLOR_GREEN}{game_mode_name}{COLOR_RESET} match!")
        print("First to reach the score wins the set." if target_wins > 1 else "")

        set_wins = 0
        set_losses = 0
        set_ties = 0

        while True:
            if target_wins > 1:
                print(f"\n{COLOR_CYAN}[Score: Player {set_wins} - {set_losses} Computer (Ties: {set_ties})]{COLOR_RESET}")

            # Check match end condition for Best-of-5
            if target_wins > 1:
                if set_wins == target_wins:
                    print(f"\n{COLOR_GREEN}{COLOR_BOLD}★ Congratulations! You won the Best-of-5 Match! ★{COLOR_RESET}")
                    stats["total_sets"] += 1
                    break
                elif set_losses == target_wins:
                    print(f"\n{COLOR_RED}{COLOR_BOLD}☠ Computer won the Best-of-5 Match! Better luck next time! ☠{COLOR_RESET}")
                    stats["total_sets"] += 1
                    break

            player_choice = get_user_choice()
            if player_choice is None:
                print(f"{COLOR_YELLOW}Exiting match set early. Scores from unfinished set are not saved.{COLOR_RESET}")
                break

            comp_choice = get_computer_choice()
            result = determine_winner(player_choice, comp_choice)

            # Print result of the round
            print_round_result(player_choice, comp_choice, result)

            # Record round statistic
            if result == "player":
                set_wins += 1
                stats["wins"] += 1
            elif result == "computer":
                set_losses += 1
                stats["losses"] += 1
            else:
                set_ties += 1
                stats["ties"] += 1

            # Single match ends after 1 round (except ties if we want a decisive winner,
            # but usually single round just finishes after 1 round).
            if target_wins == 1:
                stats["total_sets"] += 1
                break

        # Save stats instantly to file
        save_stats(stats)

        # Ask to play another game of Snake Water Gun
        again = input(f"\nWould you like to start another match? ({COLOR_GREEN}y{COLOR_RESET}/{COLOR_RED}n{COLOR_RESET}): ").strip().lower()
        if again not in ('y', 'yes'):
            break


def main():
    """
    Main function to run the application menu loop.
    """
    stats = load_stats()
    print(ASCII_ART)
    print("Welcome to Snake-Water-Gun!")

    while True:
        print(f"\n{COLOR_BOLD}{COLOR_CYAN}=== MAIN MENU ==={COLOR_RESET}")
        print("1. Play Game")
        print("2. View Rules")
        print("3. View Statistics")
        print("4. Exit")

        choice = input("Enter choice (1-4): ").strip()

        if choice == '1':
            play_game_loop(stats)
        elif choice == '2':
            print(GAME_RULES)
        elif choice == '3':
            display_stats(stats)
        elif choice == '4':
            print(f"\n{COLOR_GREEN}Thanks for playing Snake-Water-Gun! Goodbye!{COLOR_RESET}\n")
            break
        else:
            print(f"{COLOR_RED}Invalid entry. Please choose a option from 1 to 4.{COLOR_RESET}")


if __name__ == "__main__":
    main()
