"""
COMP 163 - Project 3: Quest Chronicles
Inventory System Module

Name: Darenell Curry
AI Usage: AI suggested basic add/remove mechanics and error handling.
"""

from custom_exceptions import *

MAX_INVENTORY = 20

def add_item(character, item):
    """
    Add an item to character inventory.
    Raises:
        InventoryFullError if inventory exceeds limit.
    """
    if len(character["inventory"]) >= MAX_INVENTORY:
        raise InventoryFullError("Inventory is full")
    character["inventory"].append(item)

def remove_item(character, item):
    """
    Remove an item from inventory.
    Raises ItemNotFoundError if item not in inventory.
    """
    if item not in character["inventory"]:
        raise ItemNotFoundError(f"{item} not found in inventory")
    character["inventory"].remove(item)

def use_item(character, item):
    """
    Use an item. AI suggested simple item effect mechanics.
    Currently supports:
      - "Health Potion": heals 20 HP
      - "Mana Potion": placeholder
    """
    if item not in character["inventory"]:
        raise ItemNotFoundError(f"{item} not found in inventory")
    
    if item == "Health Potion":
        character["health"] = min(character["max_health"], character["health"] + 20)
    elif item == "Mana Potion":
        pass  # Placeholder for mana system
    else:
        raise InvalidItemTypeError(f"{item} cannot be used")

    character["inventory"].remove(item)
