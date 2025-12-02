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


def accept_quest(character, quest_id, quests=None):
    if quests is None:
        quests = getattr(game_data, "QUESTS", {})

    if quest_id not in quests:
        raise QuestNotFoundError()

    quest = quests[quest_id]

    if quest_id in character["completed_quests"]:
        raise QuestAlreadyCompletedError()

    if quest_id in character["active_quests"]:
        raise QuestAlreadyAcceptedError()

    if character["level"] < quest.get("required_level", 1):
        raise InsufficientLevelError()

    prereqs = quest.get("requires", [])
    for req in prereqs:
        if req not in character["completed_quests"]:
            raise QuestRequirementsNotMetError()

    character["active_quests"].append(quest_id)


def complete_quest(character, quest_id, quests=None):
    if quests is None:
        quests = getattr(game_data, "QUESTS", {})

    if quest_id not in character["active_quests"]:
        raise QuestNotActiveError()

    quest = quests[quest_id]

    character["active_quests"].remove(quest_id)
    character["completed_quests"].append(quest_id)

    character["gold"] += quest["gold_reward"]
    character["experience"] += quest["xp_reward"]


def save_game():
    pass


def view_character_stats():
    pass
