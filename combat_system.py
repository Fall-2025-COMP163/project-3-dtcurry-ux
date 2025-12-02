"""
COMP 163 - Project 3: Quest Chronicles
Combat System Module

Name: Darenell Curry
AI Usage: AI suggested turn-based combat logic and error handling for invalid targets.
"""

from custom_exceptions import *

# ----------------------------------------------------------------------------
# COMBAT FUNCTIONS
# ----------------------------------------------------------------------------

def attack(attacker, defender):
    """
    Perform a basic attack from attacker to defender.
    Raises:
        CharacterDeadError: if attacker or defender is dead.
        InvalidTargetError: if defender is None.
    Returns damage dealt.
    """
    if attacker["health"] <= 0:
        raise CharacterDeadError(f"{attacker['name']} cannot attack while dead")
    if defender is None:
        raise InvalidTargetError("No target selected")
    if defender["health"] <= 0:
        raise CharacterDeadError(f"{defender['name']} is already dead")

    damage = max(0, attacker["attack"] - defender["defense"])
    defender["health"] = max(0, defender["health"] - damage)
    return damage

def use_ability(attacker, defender, ability):
    """
    Use a special ability during combat.
    Raises:
        AbilityOnCooldownError: if ability is on cooldown.
        CharacterDeadError: if attacker or defender is dead.
    """
    if attacker["health"] <= 0 or defender["health"] <= 0:
        raise CharacterDeadError("Cannot use ability with dead character")
    
    # AI suggested simple ability mechanics
    abilities = {
        "Fireball": 20,
        "Heal": -15,  # negative damage = heal
        "Power Strike": 25
    }

    if ability not in abilities:
        raise InvalidTargetError(f"{ability} is not a valid ability")

    damage = abilities[ability]
    if damage > 0:
        defender["health"] = max(0, defender["health"] - damage)
    else:
        attacker["health"] = min(attacker["max_health"], attacker["health"] - damage)
    
    return damage

def is_alive(character):
    """Check if a character is alive."""
    return character["health"] > 0

def battle(attacker, defender):
    """
    Simple turn-based battle simulation.
    Returns winner character dictionary.
    AI Usage: AI suggested alternating turns and simple victory condition.
    """
    while is_alive(attacker) and is_alive(defender):
        attack(attacker, defender)
        if is_alive(defender):
            attack(defender, attacker)
    return attacker if is_alive(attacker) else defender
