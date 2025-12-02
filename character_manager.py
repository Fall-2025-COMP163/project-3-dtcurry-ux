"""
COMP 163 - Project 3: Quest Chronicles
Character Manager Module

Name: Darenell Curry
AI Usage: AI suggested standard save/load routines and basic leveling logic.
"""

import json
import os
from custom_exceptions import *

SAVE_DIR = "saves"

# ----------------------------------------------------------------------------
# CHARACTER CREATION
# ----------------------------------------------------------------------------
def create_character(name, char_class):
    """
    Create a new character with default stats.
    Raises InvalidCharacterClassError if the class is invalid.
    """
    valid = ["Warrior", "Mage", "Rogue", "Cleric"]
    if char_class not in valid:
        raise InvalidCharacterClassError(f"{char_class} is not a valid class")
    
    # Default character stats
    return {
        "name": name,
        "class": char_class,
        "level": 1,
        "experience": 0,
        "gold": 0,
        "health": 100,
        "max_health": 100,
        "attack": 5,
        "defense": 2,
        "inventory": [],
        "active_quests": [],
        "completed_quests": []
    }

# ----------------------------------------------------------------------------
# SAVE AND LOAD FUNCTIONS
# ----------------------------------------------------------------------------
def save_character(character):
    """
    Save character data as JSON.
    Returns True on success.
    Raises SaveFileCorruptedError on failure.
    """
    try:
        os.makedirs(SAVE_DIR, exist_ok=True)
        path = os.path.join(SAVE_DIR, f"{character['name']}.json")
        with open(path, "w") as f:
            json.dump(character, f, indent=4)
        return True
    except Exception:
        raise SaveFileCorruptedError("Failed to save character")

def load_character(name):
    """
    Load character JSON data by name.
    Raises CharacterNotFoundError if no save exists.
    Raises SaveFileCorruptedError if file cannot be read.
    """
    path = os.path.join(SAVE_DIR, f"{name}.json")
    if not os.path.exists(path):
        raise CharacterNotFoundError(f"Character '{name}' not found")
    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        raise SaveFileCorruptedError(f"Corrupted save file for {name}")

def list_saved_characters():
    """Return a list of saved character names."""
    if not os.path.exists(SAVE_DIR):
        return []
    return [f.replace(".json", "") for f in os.listdir(SAVE_DIR)]

# ----------------------------------------------------------------------------
# CHARACTER ACTIONS
# ----------------------------------------------------------------------------
def heal_character(character, value):
    """Restore health up to max_health."""
    character["health"] = min(character["max_health"], character["health"] + value)
    return value

def gain_experience(character, xp):
    """
    Add XP and level up character automatically if threshold reached.
    Raises CharacterDeadError if character is dead.
    """
    if character["health"] <= 0:
        raise CharacterDeadError()
    character["experience"] += xp
    while character["experience"] >= 100:
        character["experience"] -= 100
        character["level"] += 1

def add_gold(character, amount):
    """Add gold to character. Dead characters cannot receive gold."""
    if character["health"] <= 0:
        raise CharacterDeadError()
    character["gold"] += amount
