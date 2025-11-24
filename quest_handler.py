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

# ============================================================================
# GAME STATE
# ============================================================================

# The currently active player character (dictionary returned by character_manager)
current_character = None

# Stores available quest definitions (loaded from game_data)
all_quests = {}

# Stores all item definitions (also provided by game_data)
all_items = {}

# Indicates whether the main game loop is running
game_running = False

# ============================================================================
# MAIN MENU
# ============================================================================

def main_menu():
    """
    Display the startup main menu and return the player's choice.

    This function loops until the user enters a valid option (1–3).
    It does not perform actions — only returns the chosen integer.
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

    - Uses character_manager.create_character() to generate character data.
    - Immediately saves the created character.
    - Enters the main game loop upon successful creation.
    """
    global current_character
    print("\n=== NEW GAME ===")
    name = input("Enter your character's name: ").strip()
    print("Choose a class: Warrior | Mage | Rogue | Cleric")
    char_class = input("Enter class: ").strip().title()

    try:
        # Attempt to create a new character through character_manager
        current_character = character_manager.create_character(name, char_class)

        # Automatically save the new character
        character_manager.save_character(current_character)
        print(f"\nCharacter '{name}' the {char_class} created successfully!")

        # Begin the game loop
        game_loop()

    except InvalidCharacterClassError as e:
        print(f"Error: {e}")


def load_game():
    """
    Load an existing saved character profile.

    - Lists available saved characters.
    - Prompts user to choose one.
    - Loads selected character via character_manager.load_character().
    - Enters the main game loop if successful.
    """
    global current_character
    print("\n=== LOAD GAME ===")

    saved_chars = character_manager.list_saved_characters()

    if not saved_chars:
        print("No saved characters found.")
        return

    # Display list of save files
    for i, char_name in enumerate(saved_chars, start=1):
        print(f"{i}. {char_name}")

    while True:
        choice = input(f"Select character (1-{len(saved_chars)}): ").strip()

        if choice.isdigit() and 1 <= int(choice) <= len(saved_chars):
            selected_name = saved_chars[int(choice) - 1]

            try:
                # Attempt to load save file
                current_character = character_manager.load_character(selected_name)
                print(f"\nLoaded character: {selected_name}")

                # Enter game loop
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

def save_game():
    raise NotImplementedError


# ============================================================================
# GAME LOOP
# ============================================================================

def game_loop():
    """
    The main gameplay loop that runs until the player chooses to quit.

    This function repeatedly:
    - Displays the in-game menu
    - Performs the chosen action
    - Auto-saves after every action
    """
    global game_running
    game_running = True

    while game_running:
        choice = game_menu()

        # Trigger game actions depending on player choice
        if choice == 1:
            view_character_stats()
        elif choice == 2:
            view_inventory()
        elif choice == 3:
            quest_menu()
        elif choice == 4:
            explore()
        elif choice == 5:
            shop()
        elif choice == 6:
            save_game()
            print("Game saved. Goodbye!")
            game_running = False

        # Automatically save after every action to prevent progress loss
        save_game()


def game_menu():
    """
    Display the main in-game menu and return the user's selection.

    Choices:
    1. Character Stats
    2. Inventory
    3. Quests
    4. Exploration / Combat
    5. Shop
    6. Save & Quit
    """
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

def view_character_stats():
    """
    Display the current character's basic stats.

    This provides a safe, read-only view so the game loop can call it
    without raising a NameError if the function was missing.
    """
    global current_character

    if not current_character:
        print("\nNo character is currently loaded.")
        return

    print("\n=== CHARACTER STATS ===")
    print(f"Name: {current_character.get('name', 'Unknown')}")
    print(f"Class: {current_character.get('class', 'Unknown')}")
    print(f"Level: {current_character.get('level', 1)}")
    print(f"HP: {current_character.get('hp', 0)}/{current_character.get('max_hp', 0)}")
    print(f"Gold: {current_character.get('gold', 0)}")

    # Print common attributes if present
    for stat in ['strength', 'dexterity', 'intelligence', 'wisdom', 'constitution', 'charisma']:
        if stat in current_character:
            print(f"{stat.capitalize()}: {current_character[stat]}")

    print(f"Active Quests: {current_character.get('active_quests', [])}")
    print(f"Completed Quests: {current_character.get('completed_quests', [])}")


def view_inventory():
    """
    Display inventory contents and allow user interactions such as:
    - Using consumables
    - Equipping items
    - Dropping items

    This menu loops until the user chooses 'Back'.
    """
    global current_character, all_items

    while True:
        print("\n=== INVENTORY MENU ===")

        # Show list of items (or a message if empty)
        if not current_character["inventory"]:
            print("Inventory is empty.")
        else:
            for i, item_id in enumerate(current_character["inventory"], start=1):
                item = all_items.get(item_id, {"name": item_id})
                print(f"{i}. {item['name']} (Type: {item.get('type', 'Unknown')})")

        # Inventory options
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
    """
    Helper function to choose an item by index.

    Returns:
        item_id (str) or None if invalid selection
    """
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
    """
    Use a consumable item, applying its effect.

    This version applies stat effects directly within this module rather than
    using inventory_system.use_item(), but preserves intended game behavior.
    """
    item_id = select_item()

    if item_id:
        item = all_items.get(item_id)

        # Only consumables may be used
        if item and item["type"] == "consumable":

            # Parse effects manually
            stat, value = item["effect"].split(":")
            value = int(value)

            # If healing, use character_manager to handle HP limits
            if stat == "health":
                healed = character_manager.heal_character(current_character, value)
                print(f"You used {item['name']} and healed {healed} HP!")
            else:
                current_character[stat] += value
                print(f"{stat.capitalize()} increased by {value}.")

            # Remove consumed item
            current_character["inventory"].remove(item_id)

        else:
            print("Item is not consumable.")


def equip_item():
    """
    Equip equipment (weapons or armor).

    This simplified version directly adjusts stats rather than using
    the full inventory_system.equip_weapon/equip_armor logic.
    """
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
    """
    Remove an item from the inventory permanently.
    """
    item_id = select_item()

    if item_id:
        current_character["inventory"].remove(item_id)
        print(f"Item '{item_id}' dropped.")


# ============================================================================
# QUEST MENU
# ============================================================================

def quest_menu():
    """
    Display quest status:

    - Active quests
    - Completed quests
    - Quests the player can start

    No quest actions are performed here — only displays information.
    """
    print("\n=== QUEST MENU ===")
    print("Active:", current_character["active_quests"])
    print("Completed:", current_character["completed_quests"])

    print("Available Quests:")
    for qid, quest in all_quests.items():
        if (qid not in current_character["active_quests"]
            and qid not in current_character["completed_quests"]):

            print(f"- {quest['title']} (Level {quest['required_level']})")

def handle_character_death():
    raise NotImplementedError


# ============================================================================
# COMBAT & EXPLORATION
# ============================================================================

def explore():
    """
    Trigger a random encounter and initiate combat.

    - An enemy matching the player's level is selected.
    - SimpleBattle manages turn-based combat.
    - Post-battle rewards or consequences are applied.
    """
    enemy = combat_system.get_random_enemy_for_level(
        current_character["level"]
    )

    battle = combat_system.SimpleBattle(current_character, enemy)

    try:
        result = battle.start_battle()

        if result["winner"] == "player":
            # Apply XP and gold rewards
            character_manager.gain_experience(current_character, result["xp_gained"])
            character_manager.add_gold(current_character, result["gold_gained"])

        elif result["winner"] == "enemy":
            # Player loses all HP — handle defeat
            handle_character_death()

    except CharacterDeadError:
        handle_character_death()


# ============================================================================
# SHOP SYSTEM
# ============================================================================

def shop():
    """
    Display shop menu where players can:
    - Buy items
    - Sell items

    Uses inventory_system for actual buy/sell logic.
    """
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
            sell_item()
        elif choice == "3":
            break
        else:
            print("Invalid choice.")


def buy_item():
    """
    Buy an item from the shop using inventory_system.buy_item().

    Handles:
    - Invalid selections
    - Insufficient gold
    - Full inventory
    - Other errors
    """
    try:
        choice = int(input("Enter item number to buy: ").strip())
        item_id = list(all_items.keys())[choice - 1]
        item = all_items[item_id]

        # Use inventory_system’s purchasing logic
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
    """
    Sell an item from the inventory using inventory_system.sell_item().

    Handles:
    - Invalid selections
    - Item not found
    - Other errors
    """
    try:
        choice = int(input("Enter item number to sell: ").strip())
        item_id = current_character["inventory"][choice - 1]
        item = all_items[item_id]

        # Use inventory_system’s selling logic
        sell_price = inventory_system.sell_item(current_character, item_id, item)

        print(f"Sold {item['name']} for {sell_price} gold.")

    except (ValueError, IndexError):
        print("Invalid selection.")
    except ItemNotFoundError:
        print("You don't have that item to sell.")
    except Exception as e:
        print(f"Could not complete sale: {e}")
