
"""
COMP 163 - Project 3: Quest Chronicles
Game Data Module

Name: [Your Name Here]
AI Usage: [Document any AI assistance used]

This module handles loading and validating game data from text files.
"""

import os
from custom_exceptions import (
    InvalidDataFormatError,
    MissingDataFileError,
    CorruptedDataError
)

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

def load_quests(filename="data/quests.txt"):
    """
    Load quest data from file.

    Expected format per quest (separated by blank lines):
    QUEST_ID: unique_quest_name
    TITLE: Quest Display Title
    DESCRIPTION: Quest description text
    REWARD_XP: 100
    REWARD_GOLD: 50
    REQUIRED_LEVEL: 1
    PREREQUISITE: previous_quest_id (or NONE)

    Returns:
        Dictionary of quests {quest_id: quest_data_dict}

    Raises:
        MissingDataFileError: If file does not exist.
        InvalidDataFormatError: If format is incorrect.
        CorruptedDataError: If file cannot be read.
    """
    if not os.path.exists(filename):
        raise MissingDataFileError(f"Quest file '{filename}' not found.")

    try:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read().strip()
    except (PermissionError, OSError, IOError) as e:
        raise CorruptedDataError(f"Could not read quest file: {e}")

    if not content:
        raise InvalidDataFormatError("Quest file is empty or invalid.")

    # Split quests by blank lines
    blocks = content.split("\n\n")
    quests = {}

    for block in blocks:
        lines = block.strip().split("\n")
        quest = parse_quest_block(lines)
        validate_quest_data(quest)
        quests[quest["quest_id"]] = quest

    return quests


def load_items(filename="data/items.txt"):
    """
    Load item data from file.

    Expected format per item (separated by blank lines):
    ITEM_ID: unique_item_name
    NAME: Item Display Name
    TYPE: weapon|armor|consumable
    EFFECT: stat_name:value (e.g., strength:5 or health:20)
    COST: 100
    DESCRIPTION: Item description

    Returns:
        Dictionary of items {item_id: item_data_dict}

    Raises:
        MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    if not os.path.exists(filename):
        raise MissingDataFileError(f"Item file '{filename}' not found.")

    try:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read().strip()
    except (PermissionError, OSError, IOError) as e:
        raise CorruptedDataError(f"Could not read item file: {e}")

    if not content:
        raise InvalidDataFormatError("Item file is empty or invalid.")

    blocks = content.split("\n\n")
    items = {}

    for block in blocks:
        lines = block.strip().split("\n")
        item = parse_item_block(lines)
        validate_item_data(item)
        items[item["item_id"]] = item

    return items


# ============================================================================
# VALIDATION FUNCTIONS
# ============================================================================

def validate_quest_data(quest_dict):
    """
    Validate that quest dictionary has all required fields.

    Required fields:
        quest_id, title, description, reward_xp, reward_gold,
        required_level, prerequisite

    Raises:
        InvalidDataFormatError if missing required fields or invalid types.
    """
    required = ["quest_id", "title", "description", "reward_xp",
                "reward_gold", "required_level", "prerequisite"]

    for field in required:
        if field not in quest_dict:
            raise InvalidDataFormatError(f"Missing field '{field}' in quest data.")

    # Check numeric fields
    for num_field in ["reward_xp", "reward_gold", "required_level"]:
        if not isinstance(quest_dict[num_field], int):
            raise InvalidDataFormatError(f"Field '{num_field}' must be an integer.")

    return True


def validate_item_data(item_dict):
    """
    Validate that item dictionary has all required fields.

    Required fields:
        item_id, name, type, effect, cost, description
    Valid types:
        weapon, armor, consumable

    Raises:
        InvalidDataFormatError if missing fields or invalid type.
    """
    required = ["item_id", "name", "type", "effect", "cost", "description"]

    for field in required:
        if field not in item_dict:
            raise InvalidDataFormatError(f"Missing field '{field}' in item data.")

    if item_dict["type"] not in ["weapon", "armor", "consumable"]:
        raise InvalidDataFormatError(f"Invalid item type: {item_dict['type']}")

    if not isinstance(item_dict["cost"], int):
        raise InvalidDataFormatError("Item cost must be an integer.")

    return True


# ============================================================================
# DEFAULT DATA CREATION
# ============================================================================

def create_default_data_files():
    """
    Create default data files if they don't exist.
    This helps with initial setup and testing.
    """
    os.makedirs("data", exist_ok=True)

    quest_file = "data/quests.txt"
    item_file = "data/items.txt"

    if not os.path.exists(quest_file):
        with open(quest_file, "w", encoding="utf-8") as f:
            f.write("""QUEST_ID: quest_intro
TITLE: Welcome Hero
DESCRIPTION: Begin your journey by speaking to the village elder.
REWARD_XP: 100
REWARD_GOLD: 50
REQUIRED_LEVEL: 1
PREREQUISITE: NONE
""")

    if not os.path.exists(item_file):
        with open(item_file, "w", encoding="utf-8") as f:
            f.write("""ITEM_ID: sword_basic
NAME: Basic Sword
TYPE: weapon
EFFECT: strength:5
COST: 100
DESCRIPTION: A simple sword for beginners.
""")


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_quest_block(lines):
    """
    Parse a block of lines into a quest dictionary.
    """
    quest = {}
    for line in lines:
        if ": " not in line:
            raise InvalidDataFormatError(f"Invalid quest line: {line}")
        key, value = line.split(": ", 1)
        key = key.strip().upper()
        value = value.strip()

        # Map keys to dictionary fields
        mapping = {
            "QUEST_ID": "quest_id",
            "TITLE": "title",
            "DESCRIPTION": "description",
            "REWARD_XP": "reward_xp",
            "REWARD_GOLD": "reward_gold",
            "REQUIRED_LEVEL": "required_level",
            "PREREQUISITE": "prerequisite"
        }

        if key not in mapping:
            raise InvalidDataFormatError(f"Unknown quest field: {key}")

        quest[mapping[key]] = value

    # Convert numeric fields
    for num_field in ["reward_xp", "reward_gold", "required_level"]:
        quest[num_field] = int(quest[num_field])

    return quest


def parse_item_block(lines):
    """
    Parse a block of lines into an item dictionary.
    """
    item = {}
    for line in lines:
        if ": " not in line:
            raise InvalidDataFormatError(f"Invalid item line: {line}")
        key, value = line.split(": ", 1)
        key = key.strip().upper()
        value = value.strip()

        mapping = {
            "ITEM_ID": "item_id",
            "NAME": "name",
            "TYPE": "type",
            "EFFECT": "effect",
            "COST": "cost",
            "DESCRIPTION": "description"
        }

        if key not in mapping:
            raise InvalidDataFormatError(f"Unknown item field: {key}")

        item[mapping[key]] = value

    # Convert cost to integer
    item["cost"] = int(item["cost"])

    return item


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== GAME DATA MODULE TEST ===")

    # Create default files for testing
    create_default_data_files()

    # Test loading quests
    try:
        quests = load_quests()
        print(f"Loaded {len(quests)} quests")
    except MissingDataFileError:
        print("Quest file not found")
    except InvalidDataFormatError as e:
        print(f"Invalid quest format: {e}")

    # Test loading items
    try:
        items = load_items()
        print(f"Loaded {len(items)} items")
    except MissingDataFileError:
        print("Item file not found")
    except InvalidDataFormatError as e:
        print(f"Invalid item format: {e}")
