"""
COMP 163 - Project 3: Quest Chronicles
Game Data Module

Name: Darenell Curry
AI Usage: AI suggested centralized data loading, quest templates, and error handling.
"""

import json
from custom_exceptions import *

DATA_FILE = "game_data.json"

# ----------------------------------------------------------------------------
# LOAD GAME DATA
# ----------------------------------------------------------------------------
def load_game_data():
    """
    Load general game data (quests, items, monsters).
    Raises:
        MissingDataFileError: if data file does not exist.
        CorruptedDataError: if data cannot be parsed.
    """
    try:
        with open(DATA_FILE) as f:
            return json.load(f)
    except FileNotFoundError:
        raise MissingDataFileError(f"{DATA_FILE} is missing")
    except json.JSONDecodeError:
        raise CorruptedDataError(f"{DATA_FILE} is corrupted")

# ----------------------------------------------------------------------------
# QUEST DATA
# ----------------------------------------------------------------------------
def get_quest_by_name(name, game_data):
    """
    Retrieve quest dictionary by name.
    Raises QuestNotFoundError if quest is not found.
    """
    quests = game_data.get("quests", [])
    for quest in quests:
        if quest["name"] == name:
            return quest
    raise QuestNotFoundError(f"Quest '{name}' not found")
