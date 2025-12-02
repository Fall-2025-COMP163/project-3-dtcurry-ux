"""
Quest Handler Module
COMP 163 - Project 3: Quest Chronicles

This module manages:
- Viewing quest status
- Accepting quests
- Completing quests
- Reward handling
"""

import game_data
from custom_exceptions import *


def view_quests(character):
    """
    Return a formatted dict of active and completed quests.
    """
    return {
        "active": character.get("active_quests", []),
        "completed": character.get("completed_quests", [])
    }


def accept_quest(character, quest_id):
    """
    Add a quest to the character's active quest list.
    """
    quests = getattr(game_data, "QUESTS", {})

    if quest_id not in quests:
        raise QuestNotFoundError(f"Quest '{quest_id}' not found.")

    if quest_id in character["active_quests"]:
        raise QuestAlreadyAcceptedError(f"Quest '{quest_id}' already active.")

    character["active_quests"].append(quest_id)


def complete_quest(character, quest_id):
    """
    Mark a quest as completed and give rewards.
    """
    quests = getattr(game_data, "QUESTS", {})

    if quest_id not in character["active_quests"]:
        raise QuestNotActiveError(f"Quest '{quest_id}' is not active.")

    quest = quests[quest_id]

    # Mark completion
    character["active_quests"].remove(quest_id)
    character["completed_quests"].append(quest_id)

    # Apply rewards
    character["gold"] += quest.get("gold_reward", 0)
    character["experience"] += quest.get("xp_reward", 0)

    return {
        "gold": quest.get("gold_reward", 0),
        "xp": quest.get("xp_reward", 0)
    }


def abandon_quest(character, quest_id):
    """
    Remove a quest from active quests without completing it.
    """
    if quest_id not in character["active_quests"]:
        raise QuestNotActiveError(f"Quest '{quest_id}' is not active.")

    character["active_quests"].remove(quest_id)


# ---------------------------------------------------------------------
# PLACEHOLDER FUNCTIONS NEEDED BY MAIN.PY (to prevent import failures)
# ---------------------------------------------------------------------

def view_character_stats():
    """Placeholder so main.py can import safely."""
    pass


def save_game():
    """Placeholder so main.py does not crash on import."""
    pass
