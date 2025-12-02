"""
COMP 163 - Project 3: Quest Chronicles
Character Manager Module

Name: [Darenell Curry]

AI Usage: [Document any AI assistance used]

This module handles character creation, loading, and saving.
"""

import json
import os
from custom_exceptions import *


SAVE_DIR = "saves"


def create_character(name, char_class):
    valid = ["Warrior", "Mage", "Rogue", "Cleric"]
    if char_class not in valid:
        raise InvalidCharacterClassError()

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


def save_character(character):
    """Must return True on success (autograder requirement)"""
    try:
        os.makedirs(SAVE_DIR, exist_ok=True)
        path = os.path.join(SAVE_DIR, f"{character['name']}.json")

        with open(path, "w") as f:
            json.dump(character, f, indent=4)

        return True

    except Exception:
        raise SaveFileWriteError()


def load_character(name):
    path = os.path.join(SAVE_DIR, f"{name}.json")

    if not os.path.exists(path):
        raise CharacterNotFoundError()

    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        raise SaveFileCorruptedError()


def list_saved_characters():
    if not os.path.exists(SAVE_DIR):
        return []
    return [f.replace(".json", "") for f in os.listdir(SAVE_DIR)]


def heal_character(character, value):
    character["health"] = min(character["max_health"], character["health"] + value)
    return value


def gain_experience(character, xp):
    if character["health"] <= 0:
        raise CharacterDeadError()

    character["experience"] += xp
    if character["experience"] >= 100:
        character["experience"] -= 100
        character["level"] += 1


def add_gold(character, amount):
    if character["health"] <= 0:
        raise CharacterDeadError()
    character["gold"] += amount
