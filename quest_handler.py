"""
COMP 163 - Project 3: Quest Chronicles
Quest Handler Module

Name: Darenell Curry
AI Usage: AI suggested quest accept/complete flow with prerequisites checks.
"""

from custom_exceptions import *

def accept_quest(character, quest):
    """
    Accept a quest and add to active_quests.
    Raises:
        QuestAlreadyAcceptedError
        QuestAlreadyCompletedError
        InsufficientLevelError if character level too low
    """
    if quest["name"] in character["active_quests"]:
        raise QuestAlreadyAcceptedError(f"{quest['name']} already active")
    if quest["name"] in character["completed_quests"]:
        raise QuestAlreadyCompletedError(f"{quest['name']} already completed")
    if character["level"] < quest.get("level_required", 1):
        raise InsufficientLevelError("Level too low for this quest")

    character["active_quests"].append(quest["name"])

def complete_quest(character, quest):
    """
    Complete a quest if in active_quests.
    Raises QuestNotActiveError if not active.
    """
    if quest["name"] not in character["active_quests"]:
        raise QuestNotActiveError(f"{quest['name']} is not active")
    character["active_quests"].remove(quest["name"])
    character["completed_quests"].append(quest["name"])
    # Reward AI-suggested: XP and gold
    character["experience"] += quest.get("reward_xp", 0)
    character["gold"] += quest.get("reward_gold", 0)
