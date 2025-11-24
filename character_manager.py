"""
COMP 163 - Project 3: Quest Chronicles
Character Manager Module

Name: [Darenell Curry]

AI Usage: [Document any AI assistance used]

This module handles character creation, loading, and saving.
"""

import os
from custom_exceptions import (
    InvalidCharacterClassError,   # Raised when an invalid class is provided
    CharacterNotFoundError,       # Raised when loading/deleting a non-existent save
    SaveFileCorruptedError,       # Raised when a file exists but can't be read
    InvalidSaveDataError,         # Raised when data is missing or wrongly formatted
    CharacterDeadError            # Raised when trying to operate on a dead character
)

# -----------------------------------------------------------------------------
# CONSTANTS
# -----------------------------------------------------------------------------

# Valid character classes with base stats.
# These values are used when creating a new character.
VALID_CLASSES = {
    "Warrior": {"health": 120, "strength": 15, "magic": 5},
    "Mage":    {"health": 80,  "strength": 8,  "magic": 20},
    "Rogue":   {"health": 90,  "strength": 12, "magic": 10},
    "Cleric":  {"health": 100, "strength": 10, "magic": 15},
}

# Required keys for the character dictionary.
# Used by validate_character_data() to check correctness.
REQUIRED_FIELDS = [
    "name", "class", "level", "health", "max_health",
    "strength", "magic", "experience", "gold",
    "inventory", "active_quests", "completed_quests"
]

# Default save directory (relative path).
DEFAULT_SAVE_DIR = "data/save_games"


# -----------------------------------------------------------------------------
# CHARACTER MANAGEMENT FUNCTIONS
# -----------------------------------------------------------------------------

def create_character(name, character_class):
    """
    Create a new character with stats based on class.

    Valid classes: Warrior, Mage, Rogue, Cleric

    Returns:
        A dictionary with character data containing:
        - name, class, level, health, max_health, strength, magic
        - experience, gold, inventory, active_quests, completed_quests

    Raises:
        InvalidCharacterClassError: If the class is not in VALID_CLASSES.
    """
    # First, ensure the class is valid.
    if character_class not in VALID_CLASSES:
        # Build a helpful error message listing valid classes.
        valid_list = ", ".join(VALID_CLASSES.keys())
        raise InvalidCharacterClassError(
            f"Invalid class '{character_class}'. Valid classes are: {valid_list}"
        )

    # Fetch base stats for the selected class.
    base = VALID_CLASSES[character_class]

    # Create and return the character dictionary.
    # Start values are simple integers and empty lists as specified.
    character = {
        "name": name,
        "class": character_class,
        "level": 1,
        "health": base["health"],
        "max_health": base["health"],
        "strength": base["strength"],
        "magic": base["magic"],
        "experience": 0,
        "gold": 100,
        "inventory": [],
        "active_quests": [],
        "completed_quests": []
    }
    return character


def save_character(character, save_directory=DEFAULT_SAVE_DIR):
    """
    Save a character to a text file.

    Filename format:
        {character_name}_save.txt

    File contents (one per line):
        NAME: character_name
        CLASS: class_name
        LEVEL: 1
        HEALTH: 120
        MAX_HEALTH: 120
        STRENGTH: 15
        MAGIC: 5
        EXPERIENCE: 0
        GOLD: 100
        INVENTORY: item1,item2
        ACTIVE_QUESTS: quest1,quest2
        COMPLETED_QUESTS: questA

    Returns:
        True if the save was successful.

    Raises:
        PermissionError, IOError: These are allowed to propagate naturally.
        InvalidSaveDataError: If the character data is invalid before saving.
    """
    # Validate the character before writing to disk.
    validate_character_data(character)

    # Ensure the save directory exists. If not, create it.
    os.makedirs(save_directory, exist_ok=True)

    # Build the save file path using the character's name.
    filename = os.path.join(save_directory, f"{character['name']}_save.txt")

    # Helper: convert lists to comma-separated strings (empty list -> empty string).
    def list_to_csv(lst):
        if lst:
            # Use str(x) in case items are not strings.
            return ",".join(str(x).strip() for x in lst)
        return ""

    # Create the lines to write exactly in the expected format.
    lines = [
        f"NAME: {character['name']}",
        f"CLASS: {character['class']}",
        f"LEVEL: {character['level']}",
        f"HEALTH: {character['health']}",
        f"MAX_HEALTH: {character['max_health']}",
        f"STRENGTH: {character['strength']}",
        f"MAGIC: {character['magic']}",
        f"EXPERIENCE: {character['experience']}",
        f"GOLD: {character['gold']}",
        f"INVENTORY: {list_to_csv(character['inventory'])}",
        f"ACTIVE_QUESTS: {list_to_csv(character['active_quests'])}",
        f"COMPLETED_QUESTS: {list_to_csv(character['completed_quests'])}",
    ]

    # Write the file. Let I/O exceptions propagate (as assignment allows).
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return True


def load_character(character_name, save_directory=DEFAULT_SAVE_DIR):
    """
    Load a character from a save file.

    Args:
        character_name: The name of the character to load.
        save_directory: The directory containing save files.

    Returns:
        A character dictionary.

    Raises:
        CharacterNotFoundError: If the save file doesn't exist.
        SaveFileCorruptedError: If the file exists but can't be read.
        InvalidSaveDataError: If the file contents are missing or invalid.
    """
    # Build the expected file path.
    filename = os.path.join(save_directory, f"{character_name}_save.txt")

    # If the file doesn't exist, we can't load this character.
    if not os.path.exists(filename):
        raise CharacterNotFoundError(f"No save file found for '{character_name}'.")

    # Try reading the file. If reading fails, the file may be corrupted or restricted.
    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()  # Keep lines without trailing newline
    except (PermissionError, OSError, IOError) as e:
        raise SaveFileCorruptedError(f"Could not read save file: {e}")

    # Parse "KEY: value" lines into a temporary dictionary.
    data = {}
    key_map = {
        "NAME": "name",
        "CLASS": "class",
        "LEVEL": "level",
        "HEALTH": "health",
        "MAX_HEALTH": "max_health",
        "STRENGTH": "strength",
        "MAGIC": "magic",
        "EXPERIENCE": "experience",
        "GOLD": "gold",
        "INVENTORY": "inventory",
        "ACTIVE_QUESTS": "active_quests",
        "COMPLETED_QUESTS": "completed_quests",
    }

    for line in lines:
        # Each valid line should contain a colon.
        if ":" not in line:
            raise InvalidSaveDataError(f"Invalid line format: '{line}'")
        # Split into key and value only at the first colon.
        key, value = line.split(":", 1)
        key = key.strip().upper()   # Standardize to uppercase for matching key_map
        value = value.strip()       # Remove surrounding spaces from the value

        # Ensure the key is one we recognize.
        if key not in key_map:
            raise InvalidSaveDataError(f"Unknown field '{key}' in save file.")

        # Store the raw string value (convert types below).
        data[key_map[key]] = value

    # Confirm all required fields were present in the file.
    missing_fields = []
    for field in REQUIRED_FIELDS:
        if field not in data:
            missing_fields.append(field)
    if missing_fields:
        raise InvalidSaveDataError(
            f"Missing fields in save data: {', '.join(missing_fields)}"
        )

    # Convert numeric strings to integers. If conversion fails, the file is invalid.
    int_fields = ["level", "health", "max_health", "strength", "magic", "experience", "gold"]
    for field in int_fields:
        try:
            data[field] = int(data[field])
        except ValueError:
            raise InvalidSaveDataError(
                f"Field '{field}' must be an integer. Got '{data[field]}'."
            )

    # Convert comma-separated lists back into Python lists.
    # Empty string should become an empty list.
    list_fields = ["inventory", "active_quests", "completed_quests"]
    for field in list_fields:
        raw = data[field]
        if raw == "":
            data[field] = []
        else:
            # Split by commas, strip spaces, and ignore empty entries.
            items = raw.split(",")
            clean_items = []
            for item in items:
                item = item.strip()
                if item != "":
                    clean_items.append(item)
            data[field] = clean_items

    # Final validation of loaded character data.
    validate_character_data(data)

    return data


def list_saved_characters(save_directory=DEFAULT_SAVE_DIR):
    """
    Get a list of all saved character names.

    The function checks the save directory for files ending with "_save.txt"
    and returns the character names without the suffix.

    Returns:
        A list of names. Returns an empty list if the directory doesn't exist.
    """
    # If the directory doesn't exist, there are no saved characters.
    if not os.path.isdir(save_directory):
        return []

    names = []
    for fname in os.listdir(save_directory):
        # Only consider files that end exactly with "_save.txt".
        if fname.endswith("_save.txt"):
            # Remove the last 9 characters (length of "_save.txt") to get the name.
            names.append(fname[:-9])

    return names


def delete_character(character_name, save_directory=DEFAULT_SAVE_DIR):
    """
    Delete a character's save file.

    Returns:
        True if the file was deleted.

    Raises:
        CharacterNotFoundError: If the save file doesn't exist.
    """
    filename = os.path.join(save_directory, f"{character_name}_save.txt")

    # Ensure the file exists before trying to remove it.
    if not os.path.exists(filename):
        raise CharacterNotFoundError(f"No save file found for '{character_name}'.")

    # Remove the file from the directory.
    os.remove(filename)
    return True


# -----------------------------------------------------------------------------
# CHARACTER OPERATIONS
# -----------------------------------------------------------------------------

def gain_experience(character, xp_amount):
    """
    Add experience points to a character and handle level ups.

    Level up formula:
        Required XP for next level = current_level * 100

    On level up:
        - Increase level by 1
        - Increase max_health by 10
        - Increase strength by 2
        - Increase magic by 2
        - Restore health to max_health

    Returns:
        True if at least one level-up occurred, False otherwise.

    Raises:
        CharacterDeadError: If the character's health is 0 or below.
        InvalidSaveDataError: If xp_amount is not a non-negative integer.
    """
    # Dead characters should not gain XP.
    if is_character_dead(character):
        raise CharacterDeadError(f"{character['name']} is dead and cannot gain experience.")

    # xp_amount must be a non-negative integer.
    if not isinstance(xp_amount, int):
        raise InvalidSaveDataError("Experience amount must be an integer.")
    if xp_amount < 0:
        raise InvalidSaveDataError("Experience amount cannot be negative.")

    # Add the experience.
    character["experience"] += xp_amount

    # Track if any level-up happens.
    leveled_up = False

    # Keep leveling while experience meets/exceeds the current threshold.
    # This allows multiple level-ups at once if a big XP reward is given.
    while character["experience"] >= character["level"] * 100:
        required = character["level"] * 100
        character["experience"] -= required
        character["level"] += 1
        character["max_health"] += 10
        character["strength"] += 2
        character["magic"] += 2
        character["health"] = character["max_health"]  # restore full HP on level-up
        leveled_up = True

    return leveled_up


def add_gold(character, amount):
    """
    Add gold to the character's gold total. Negative amounts spend gold.

    Args:
        character: The character dictionary to modify.
        amount: The integer amount of gold to add or subtract.

    Returns:
        The new gold total after the operation.

    Raises:
        InvalidSaveDataError: If amount is not an integer.
        ValueError: If the operation would make gold negative.
    """
    # Amount must be an integer (zyBooks-level validation).
    if not isinstance(amount, int):
        raise InvalidSaveDataError("Gold amount must be an integer.")

    # Compute the new total and ensure it is not negative.
    new_total = character["gold"] + amount
    if new_total < 0:
        raise ValueError("Cannot reduce gold below 0.")

    # Update and return the new total.
    character["gold"] = new_total
    return character["gold"]


def heal_character(character, amount):
    """
    Heal a character by a specific amount without exceeding max_health.

    Args:
        character: The character dictionary to heal.
        amount: The integer amount of health to restore.

    Returns:
        The actual amount of healing applied (may be less than requested).

    Raises:
        InvalidSaveDataError: If amount is not an integer.
    """
    # Heal amount must be a positive integer to have an effect.
    if not isinstance(amount, int):
        raise InvalidSaveDataError("Heal amount must be an integer.")
    if amount <= 0:
        # Non-positive amounts do not heal; return 0 for clarity.
        return 0

    # Calculate how much health is missing.
    missing = character["max_health"] - character["health"]

    # Actual healing is the smaller of the requested amount and missing health.
    actual = amount if amount <= missing else missing

    # Apply the healing.
    character["health"] += actual

    return actual


def is_character_dead(character):
    """
    Check whether a character is dead.

    A character is considered dead if health is 0 or below.

    Returns:
        True if the character is dead, False if alive.
    """
    # Use get() with default 0 to avoid KeyErrors if called early.
    return character.get("health", 0) <= 0


def revive_character(character):
    """
    Revive a dead character to 50% of max_health (rounded down).

    If the character is already alive, no changes are made.

    Returns:
        True if the character was revived, False if the character was already alive.
    """
    # Only revive if dead.
    if not is_character_dead(character):
        return False

    # Calculate half of max health using integer division.
    half = character["max_health"] // 2

    # Make sure revived characters have at least 1 HP.
    if half < 1:
        half = 1

    character["health"] = half
    return True


# -----------------------------------------------------------------------------
# VALIDATION
# -----------------------------------------------------------------------------

def validate_character_data(character):
    """
    Validate that a character dictionary has all required fields and types.

    Required fields:
        name, class, level, health, max_health, strength, magic,
        experience, gold, inventory, active_quests, completed_quests

    Returns:
        True if the character data is valid.

    Raises:
        InvalidSaveDataError: If fields are missing or types/values are invalid.
    """
    # Check that all required keys exist in the dictionary.
    missing = []
    for key in REQUIRED_FIELDS:
        if key not in character:
            missing.append(key)
    if missing:
        raise InvalidSaveDataError(f"Character data missing fields: {', '.join(missing)}")

    # Strings: name and class must be non-empty strings.
    if not isinstance(character["name"], str) or character["name"] == "":
        raise InvalidSaveDataError("Field 'name' must be a non-empty string.")
    if not isinstance(character["class"], str) or character["class"] == "":
        raise InvalidSaveDataError("Field 'class' must be a non-empty string.")

    # Numbers: ensure all numeric fields are integers.
    numeric_fields = ["level", "health", "max_health", "strength", "magic", "experience", "gold"]
    for field in numeric_fields:
        if not isinstance(character[field], int):
            raise InvalidSaveDataError(f"Field '{field}' must be an integer.")

    # Lists: ensure list fields are actual lists.
    list_fields = ["inventory", "active_quests", "completed_quests"]
    for field in list_fields:
        if not isinstance(character[field], list):
            raise InvalidSaveDataError(f"Field '{field}' must be a list.")

    # Logical checks for reasonable values.
    if character["level"] < 1:
        raise InvalidSaveDataError("Level must be at least 1.")
    if character["max_health"] <= 0:
        raise InvalidSaveDataError("Max health must be positive.")
    if character["health"] < 0:
        raise InvalidSaveDataError("Health cannot be negative.")
    if character["health"] > character["max_health"]:
        raise InvalidSaveDataError("Health cannot exceed max_health.")
    if character["gold"] < 0:
        raise InvalidSaveDataError("Gold cannot be negative.")

    # If we reached here, everything is valid.
    return True


# -----------------------------------------------------------------------------
# SIMPLE TESTING (OPTIONAL)
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    print("=== CHARACTER MANAGER TEST ===")

    # Create a test character.
    try:
        char = create_character("TestHero", "Warrior")
        print(f"Created: {char['name']} the {char['class']}")
        print(f"Stats: HP={char['health']}/{char['max_health']}, STR={char['strength']}, "
              f"MAG={char['magic']}, XP={char['experience']}, GOLD={char['gold']}")
    except InvalidCharacterClassError as e:
        print(f"Invalid class: {e}")

    # Gain some experience and check for level-ups.
    try:
        leveled = gain_experience(char, 250)  # 100 (lvl 1) + 200 (lvl 2) -> two level-ups
        print(f"Leveled up? {leveled}")
        print(f"After XP: level={char['level']}, HP={char['health']}/{char['max_health']}, "
              f"STR={char['strength']}, MAG={char['magic']}, XP={char['experience']}")
    except CharacterDeadError as e:
        print(f"Cannot gain XP: {e}")
    except InvalidSaveDataError as e:
        print(f"XP error: {e}")

    # Save the character.
    try:
        save_character(char)
        print("Character saved successfully.")
    except Exception as e:
        print(f"Save error: {e}")

    # Load the character back.
    try:
        loaded = load_character("TestHero")
        print(f"Loaded: {loaded['name']} lvl {loaded['level']}, class {loaded['class']}")
    except CharacterNotFoundError:
        print("Character not found")
    except SaveFileCorruptedError:
        print("Save file corrupted")
    except InvalidSaveDataError as e:
        print(f"Invalid save data: {e}")

    # List and then delete test character.
    print("Saved characters:", list_saved_characters())
    try:
        delete_character("TestHero")
        print("Deleted 'TestHero'.")
    except CharacterNotFoundError as e:
        print(e)
    # TODO: Implement character creation
    # Validate character_class first
    # Example base stats:
    # Warrior: health=120, strength=15, magic=5
    # Mage: health=80, strength=8, magic=20
    # Rogue: health=90, strength=12, magic=10
    # Cleric: health=100, strength=10, magic=15
    
    # All characters start with:
    # - level=1, experience=0, gold=100
    # - inventory=[], active_quests=[], completed_quests=[]
    
    # Raise InvalidCharacterClassError if class not in valid list
    pass

def save_character(character, save_directory="data/save_games"):
    """
    Save character to file
    
    Filename format: {character_name}_save.txt
    
    File format:
    NAME: character_name
    CLASS: class_name
    LEVEL: 1
    HEALTH: 120
    MAX_HEALTH: 120
    STRENGTH: 15
    MAGIC: 5
    EXPERIENCE: 0
    GOLD: 100
    INVENTORY: item1,item2,item3
    ACTIVE_QUESTS: quest1,quest2
    COMPLETED_QUESTS: quest1,quest2
    
    Returns: True if successful
    Raises: PermissionError, IOError (let them propagate or handle)
    """
    # TODO: Implement save functionality
    # Create save_directory if it doesn't exist
    # Handle any file I/O errors appropriately
    # Lists should be saved as comma-separated values
    pass

def load_character(character_name, save_directory="data/save_games"):
    """
    Load character from save file
    
    Args:
        character_name: Name of character to load
        save_directory: Directory containing save files
    
    Returns: Character dictionary
    Raises: 
        CharacterNotFoundError if save file doesn't exist
        SaveFileCorruptedError if file exists but can't be read
        InvalidSaveDataError if data format is wrong
    """
    # TODO: Implement load functionality
    # Check if file exists → CharacterNotFoundError
    # Try to read file → SaveFileCorruptedError
    # Validate data format → InvalidSaveDataError
    # Parse comma-separated lists back into Python lists
    pass

def list_saved_characters(save_directory="data/save_games"):
    """
    Get list of all saved character names
    
    Returns: List of character names (without _save.txt extension)
    """
    # TODO: Implement this function
    # Return empty list if directory doesn't exist
    # Extract character names from filenames
    pass

def delete_character(character_name, save_directory="data/save_games"):
    """
    Delete a character's save file
    
    Returns: True if deleted successfully
    Raises: CharacterNotFoundError if character doesn't exist
    """
    # TODO: Implement character deletion
    # Verify file exists before attempting deletion
    pass

# ============================================================================
# CHARACTER OPERATIONS
# ============================================================================

def gain_experience(character, xp_amount):
    """
    Add experience to character and handle level ups
    
    Level up formula: level_up_xp = current_level * 100
    Example when leveling up:
    - Increase level by 1
    - Increase max_health by 10
    - Increase strength by 2
    - Increase magic by 2
    - Restore health to max_health
    
    Raises: CharacterDeadError if character health is 0
    """
    # TODO: Implement experience gain and leveling
    # Check if character is dead first
    # Add experience
    # Check for level up (can level up multiple times)
    # Update stats on level up
    pass

def add_gold(character, amount):
    """
    Add gold to character's inventory
    
    Args:
        character: Character dictionary
        amount: Amount of gold to add (can be negative for spending)
    
    Returns: New gold total
    Raises: ValueError if result would be negative
    """
    # TODO: Implement gold management
    # Check that result won't be negative
    # Update character's gold
    pass

def heal_character(character, amount):
    """
    Heal character by specified amount
    
    Health cannot exceed max_health
    
    Returns: Actual amount healed
    """
    # TODO: Implement healing
    # Calculate actual healing (don't exceed max_health)
    # Update character health
    pass

def is_character_dead(character):
    """
    Check if character's health is 0 or below
    
    Returns: True if dead, False if alive
    """
    # TODO: Implement death check
    pass

def revive_character(character):
    """
    Revive a dead character with 50% health
    
    Returns: True if revived
    """
    # TODO: Implement revival
    # Restore health to half of max_health
    pass

# ============================================================================
# VALIDATION
# ============================================================================

def validate_character_data(character):
    """
    Validate that character dictionary has all required fields
    
    Required fields: name, class, level, health, max_health, 
                    strength, magic, experience, gold, inventory,
                    active_quests, completed_quests
    
    Returns: True if valid
    Raises: InvalidSaveDataError if missing fields or invalid types
    """
    # TODO: Implement validation
    # Check all required keys exist
    # Check that numeric values are numbers
    # Check that lists are actually lists
    pass

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== CHARACTER MANAGER TEST ===")
    
    # Test character creation
    # try:
    #     char = create_character("TestHero", "Warrior")
    #     print(f"Created: {char['name']} the {char['class']}")
    #     print(f"Stats: HP={char['health']}, STR={char['strength']}, MAG={char['magic']}")
    # except InvalidCharacterClassError as e:
    #     print(f"Invalid class: {e}")
    
    # Test saving
    # try:
    #     save_character(char)
    #     print("Character saved successfully")
    # except Exception as e:
    #     print(f"Save error: {e}")
    
    # Test loading
    # try:
    #     loaded = load_character("TestHero")
    #     print(f"Loaded: {loaded['name']}")
    # except CharacterNotFoundError:
    #     print("Character not found")
    # except SaveFileCorruptedError:
    #     print("Save file corrupted")

