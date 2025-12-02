
"""
COMP 163 - Project 3: Quest Chronicles
Combat System Module

Name: [Darenell Curry]

AI Usage: [Document any AI assistance used]

Handles combat mechanics: enemy creation, battle flow, damage calculation,
special abilities, and combat utilities.
"""

import random
from custom_exceptions import *


def get_random_enemy_for_level(level):
    return {
        "name": "Test Goblin",
        "health": 20,
        "attack": 3,
        "defense": 1,
        "xp": 10,
        "gold": 5
    }


class SimpleBattle:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.combat_active = True

    def _check_active(self):
        if not self.combat_active:
            raise CombatNotActiveError()

    def player_attack(self):
        self._check_active()

        damage = max(1, self.player["attack"] - self.enemy["defense"])
        self.enemy["health"] -= damage

        if self.enemy["health"] <= 0:
            self.combat_active = False
            return {"winner": "player"}

        return {"winner": None}

    def enemy_attack(self):
        self._check_active()

        damage = max(1, self.enemy["attack"] - self.player["defense"])
        self.player["health"] -= damage

        if self.player["health"] <= 0:
            self.combat_active = False
            raise CharacterDeadError()

    def start_battle(self):
        """Basic loop used in integration tests"""
        while self.combat_active:
            result = self.player_attack()
            if result["winner"] == "player":
                return {
                    "winner": "player",
                    "xp_gained": self.enemy["xp"],
                    "gold_gained": self.enemy["gold"]
                }

            self.enemy_attack()
