"""
COMP 163 - Project 3: Quest Chronicles
Main Game Module

Name: [Your Name Here]
AI Usage: ChatGPT used to help write explanatory comments and ensure clarity
across the module. All game logic and structure remain student-authored.

This module ties all other game modules together and provides the main
interface the player interacts with:
- Character creation and loading
- Inventory management
- Quests
- Combat
- Shopping
- Saving and loading game state
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

# Active player character (populated by new_game/load_game)
current_character = None

# Load all static data from game_data safely
all_items = deepcopy(getattr(game_data, "ITEMS", {}))
all_quests = deepcopy(getattr(game_data, "QUESTS", {}))
all_enemies = deepcopy(getattr(game_data, "ENEMIES", {}))

# Track whether main loop is running
game_running = False

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

    for i, char_name in enumerate(saved_chars, start=1):
        print(f"{i}. {char_name}")

    while True:
        choice = input(f"Select character (1-{len(saved_chars)}): ").strip()

        if choice.isdigit() and 1 <= int(choice) <= len(saved_chars):
            selected_name = saved_chars[int(choice) - 1]
            try:
                current_character = character_manager.load_character(selected_name)
                print(f"\nLoaded character: {selected_name}")
                game_loop()
                break

            except CharacterNotFoundError:
                print("Character not found.")
                break

            except SaveFileCorruptedError:
                print("Save file corrupted.")
                break

        else:
            print("Invalid choice.")


# ============================================================================
# GAME LOOP
# ============================================================================

def game_loop():
    """
    Repeatedly display the game menu and execute actions
    until the player chooses to save & quit.
    """
    global game_running
    game_running = True

    while game_running:
        choice = game_menu()

        if choice == 1:
            quest_handler.view_character_stats()
        elif choice == 2:
            view_inventory()
        elif choice == 3:
            quest_menu()
        elif choice == 4:
            explore()
        elif choice == 5:
            shop()
        elif choice == 6:
            quest_handler.save_game()
            print("Game saved. Goodbye!")
            game_running = False

        # Auto-save
        quest_handler.save_game()


def game_menu():
    """Show in-game options and return player's selection."""
    print("\n=== GAME MENU ===")
    print("1. View Character Stats")
    print("2. View Inventory")
    print("3. Quest Menu")
    print("4. Explore (Find Battles)")
    print("5. Shop")
    print("6. Save and Quit")

    while True:
        choice = input("Enter choice (1-6): ").strip()
        if choice in ["1", "2", "3", "4", "5", "6"]:
            return int(choice)
        print("Invalid choice.")


# ============================================================================
# INVENTORY MANAGEMENT
# ============================================================================

def view_inventory():
    """Display and manage inventory actions."""
    global current_character, all_items

    while True:
        print("\n=== INVENTORY MENU ===")

        if not current_character["inventory"]:
            print("Inventory is empty.")
        else:
            for i, item_id in enumerate(current_character["inventory"], start=1):
                item = all_items.get(item_id, {"name": item_id})
                print(f"{i}. {item['name']} (Type: {item.get('type', 'Unknown')})")

        print("\nOptions:")
        print("1. Use Item")
        print("2. Equip Item")
        print("3. Drop Item")
        print("4. Back")

        choice = input("Enter choice (1-4): ").strip()

        if choice == "1":
            use_item()
        elif choice == "2":
            equip_item()
        elif choice == "3":
            drop_item()
        elif choice == "4":
            break
        else:
            print("Invalid choice.")


def select_item():
    """Helper for choosing an item by number."""
    if not current_character["inventory"]:
        return None

    try:
        choice = int(input("Select item number: ").strip())
        if 1 <= choice <= len(current_character["inventory"]):
            return current_character["inventory"][choice - 1]
        print("Invalid selection.")
        return None

    except ValueError:
        print("Invalid input.")
        return None


def use_item():
    """Use a consumable item and apply its effects."""
    item_id = select_item()

    if item_id:
        item = all_items.get(item_id)

        if item and item["type"] == "consumable":
            stat, value = item["effect"].split(":")
            value = int(value)

            if stat == "health":
                healed = character_manager.heal_character(current_character, value)
                print(f"You used {item['name']} and healed {healed} HP!")
            else:
                current_character[stat] += value
                print(f"{stat.capitalize()} increased by {value}.")

            current_character["inventory"].remove(item_id)

        else:
            print("Item is not consumable.")


def equip_item():
    """Equip a weapon or armor and apply stat bonus."""
    item_id = select_item()

    if item_id:
        item = all_items.get(item_id)

        if item and item["type"] in ["weapon", "armor"]:
            stat, value = item["effect"].split(":")
            value = int(value)

            current_character[stat] += value
            print(f"You equipped {item['name']}! {stat.capitalize()} +{value}.")
        else:
            print("Item cannot be equipped.")


def drop_item():
    """Drop an item permanently."""
    item_id = select_item()

    if item_id:
        current_character["inventory"].remove(item_id)
        print(f"Item '{item_id}' dropped.")


# ============================================================================
# QUEST MENU
# ============================================================================

def quest_menu():
    """Display quest status and available quests."""
    print("\n=== QUEST MENU ===")
    print("Active:", current_character["active_quests"])
    print("Completed:", current_character["completed_quests"])

    print("Available Quests:")
    for qid, quest in all_quests.items():
        if (qid not in current_character["active_quests"]
            and qid not in current_character["completed_quests"]):
            print(f"- {quest['title']} (Level {quest['required_level']})")


def handle_character_death():
    """Placeholder for death behavior (respawn, reload, etc)."""
    raise NotImplementedError


# ============================================================================
# COMBAT & EXPLORATION
# ============================================================================

def explore():
    """Find an enemy and begin combat."""
    enemy = combat_system.get_random_enemy_for_level(
        current_character["level"]
    )

    battle = combat_system.SimpleBattle(current_character, enemy)

    try:
        result = battle.start_battle()

        if result["winner"] == "player":
            character_manager.gain_experience(current_character, result["xp_gained"])
            character_manager.add_gold(current_character, result["gold_gained"])

        elif result["winner"] == "enemy":
            handle_character_death()

    except CharacterDeadError:
        handle_character_death()


# ============================================================================
# SHOP SYSTEM
# ============================================================================

def shop():
    """Shop for items using inventory_system logic."""
    global current_character, all_items

    while True:
        print("\n=== SHOP ===")
        print(f"Gold: {current_character['gold']}")

        print("Items for Sale:")
        for i, (item_id, item) in enumerate(all_items.items(), start=1):
            print(f"{i}. {item['name']} - {item['cost']} gold")

        print("\nOptions:")
        print("1. Buy Item")
        print("2. Sell Item")
        print("3. Back")

        choice = input("Enter choice (1-3): ").strip()

        if choice == "1":
            buy_item()
        elif choice == "2":
            quest_handler.sell_item()
        elif choice == "3":
            break
        else:
            print("Invalid choice.")


def buy_item():
    """Buy an item safely with error handling."""
    try:
        choice = int(input("Enter item number to buy: ").strip())
        item_id = list(all_items.keys())[choice - 1]
        item = all_items[item_id]

        inventory_system.buy_item(current_character, item_id, item)
        print(f"Bought {item['name']} for {item['cost']} gold.")

    except (ValueError, IndexError):
        print("Invalid selection.")
    except InsufficientFundsError:
        print("You don't have enough gold to buy that item.")
    except InventoryFullError:
        print("Your inventory is full. Drop something before buying.")
    except Exception as e:
        print(f"Could not complete purchase: {e}")
def sell_item():
    """Sell an item safely with error handling."""
    try:
        choice = int(input("Enter item number to sell: ").strip())
        item_id = current_character["inventory"][choice - 1]
        item = all_items.get(item_id)

        if not item:
            print("Item data not found.")
            return

        sell_price = inventory_system.sell_item(current_character, item_id, item)
        print(f"Sold {item['name']} for {sell_price} gold.")

    except (ValueError, IndexError):
        print("Invalid selection.")
    except ItemNotFoundError:
        print("You don't have that item to sell.")
    except Exception as e:
        print(f"Could not complete sale: {e}")
