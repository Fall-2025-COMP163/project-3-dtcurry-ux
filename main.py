"""
COMP 163 - Project 3: Quest Chronicles
Main Game Module

Name: [Your Name Here]
AI Usage: ChatGPT used to help write explanatory comments and ensure clarity
across the module. All game logic and structure remain student-authored.
"""

import character_manager
import inventory_system
import quest_handler
import combat_system
import game_data
from custom_exceptions import *

from copy import deepcopy

# ============================================================================
# GAME STATE INITIALIZATION
# ============================================================================

current_character = None
game_running = False

def load_game_data():
    """
    Load static game data from game_data safely.
    """
    global all_items, all_quests, all_enemies

    all_items = deepcopy(getattr(game_data, "ITEMS", {}))
    all_quests = deepcopy(getattr(game_data, "QUESTS", {}))
    all_enemies = deepcopy(getattr(game_data, "ENEMIES", {}))

# Initialize empty defaults so module imports cleanly
all_items = {}
all_quests = {}
all_enemies = {}

# ============================================================================
# MAIN MENU
# ============================================================================

def main_menu():
    """
    Display the startup main menu and return the player's choice.
    """
    print("\n=== MAIN MENU ===")
    print("1. New Game")
    print("2. Load Game")
    print("3. Exit")

    while True:
        choice = input("Enter choice (1-3): ").strip()
        if choice in ["1", "2", "3"]:
            return int(choice)
        print("Invalid choice. Please enter 1, 2, or 3.")


def new_game():
    """
    Start a new game by prompting the user for a character name and class.
    """
    global current_character
    print("\n=== NEW GAME ===")
    name = input("Enter your character's name: ").strip()
    print("Choose a class: Warrior | Mage | Rogue | Cleric")
    char_class = input("Enter class: ").strip().title()

    try:
        current_character = character_manager.create_character(name, char_class)
        character_manager.save_character(current_character)
        print(f"\nCharacter '{name}' the {char_class} created successfully!")
        game_loop()

    except InvalidCharacterClassError as e:
        print(f"Error: {e}")


def save_game():
    """Save current game state to character file."""
    global current_character

    if current_character is None:
        print("No character to save.")
        return

    try:
        character_manager.save_character(current_character)
        print("Game saved successfully!")
    except SaveFileWriteError as e:
        print(f"Error saving game: {e}")


def load_game():
    """
    Load an existing saved character.
    """
    global current_character
    print("\n=== LOAD GAME ===")

    saved_chars = character_manager.list_saved_characters()
    if not saved_chars:
        print("No saved characters found.")
        return
