"""
COMP 163 - Project 3: Quest Chronicles
Inventory System Module - Completed Implementation

Name: [Your Name Here]

AI Usage: ChatGPT assisted in implementing logic, validating edge cases, 
and ensuring consistency with project specifications.
"""

from custom_exceptions import (
    InventoryFullError,
    ItemNotFoundError,
    InsufficientResourcesError,
    InvalidItemTypeError
)

# Maximum inventory size
MAX_INVENTORY_SIZE = 20

# ============================================================================
# INVENTORY MANAGEMENT
# ============================================================================

def add_item_to_inventory(character, item_id):
    """
    Add an item to character's inventory
    """
    if len(character["inventory"]) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory is full")

    character["inventory"].append(item_id)
    return True


def remove_item_from_inventory(character, item_id):
    """
    Remove an item from character's inventory
    """
    if item_id not in character["inventory"]:
        raise ItemNotFoundError(f"Item '{item_id}' not found")

    character["inventory"].remove(item_id)
    return True


def has_item(character, item_id):
    """
    Check if character has a specific item
    """
    return item_id in character["inventory"]


def count_item(character, item_id):
    """
    Count occurrences of item in inventory
    """
    return character["inventory"].count(item_id)


def get_inventory_space_remaining(character):
    """
    Return available inventory slots
    """
    return MAX_INVENTORY_SIZE - len(character["inventory"])


def clear_inventory(character):
    """
    Remove all items
    """
    removed = character["inventory"][:]
    character["inventory"].clear()
    return removed

# ============================================================================
# ITEM USAGE
# ============================================================================

def use_item(character, item_id, item_data):
    """
    Use a consumable item
    """
    if not has_item(character, item_id):
        raise ItemNotFoundError(f"Item '{item_id}' not found")

    if item_data["type"] != "consumable":
        raise InvalidItemTypeError(f"Item '{item_id}' is not consumable")

    stat, value = parse_item_effect(item_data["effect"])
    apply_stat_effect(character, stat, value)

    remove_item_from_inventory(character, item_id)
    return f"Used {item_id}! {stat} increased by {value}."


def equip_weapon(character, item_id, item_data):
    """
    Equip a weapon
    """
    if not has_item(character, item_id):
        raise ItemNotFoundError(f"Weapon '{item_id}' not found")

    if item_data["type"] != "weapon":
        raise InvalidItemTypeError("Item is not a weapon")

    # Unequip current
    if character.get("equipped_weapon"):
        old_weapon = character["equipped_weapon"]
        old_stat, old_val = parse_item_effect(character["equipped_weapon_effect"])

        apply_stat_effect(character, old_stat, -old_val)
        add_item_to_inventory(character, old_weapon)

    # Equip new
    stat, value = parse_item_effect(item_data["effect"])
    apply_stat_effect(character, stat, value)

    character["equipped_weapon"] = item_id
    character["equipped_weapon_effect"] = item_data["effect"]

    remove_item_from_inventory(character, item_id)
    return f"Equipped weapon: {item_id} (+{value} {stat})."


def equip_armor(character, item_id, item_data):
    """
    Equip armor
    """
    if not has_item(character, item_id):
        raise ItemNotFoundError(f"Armor '{item_id}' not found")

    if item_data["type"] != "armor":
        raise InvalidItemTypeError("Item is not armor")

    # Unequip current
    if character.get("equipped_armor"):
        old_armor = character["equipped_armor"]
        old_stat, old_val = parse_item_effect(character["equipped_armor_effect"])

        apply_stat_effect(character, old_stat, -old_val)
        add_item_to_inventory(character, old_armor)

    # Equip new
    stat, value = parse_item_effect(item_data["effect"])
    apply_stat_effect(character, stat, value)

    character["equipped_armor"] = item_id
    character["equipped_armor_effect"] = item_data["effect"]

    remove_item_from_inventory(character, item_id)
    return f"Equipped armor: {item_id} (+{value} {stat})."


def unequip_weapon(character):
    """
    Unequip weapon
    """
    if not character.get("equipped_weapon"):
        return None

    weapon = character["equipped_weapon"]
    stat, value = parse_item_effect(character["equipped_weapon_effect"])

    apply_stat_effect(character, stat, -value)

    if get_inventory_space_remaining(character) <= 0:
        raise InventoryFullError("Cannot unequip, inventory full")

    add_item_to_inventory(character, weapon)
    character["equipped_weapon"] = None
    character["equipped_weapon_effect"] = None

    return weapon


def unequip_armor(character):
    """
    Unequip armor
    """
    if not character.get("equipped_armor"):
        return None

    armor = character["equipped_armor"]
    stat, value = parse_item_effect(character["equipped_armor_effect"])

    apply_stat_effect(character, stat, -value)

    if get_inventory_space_remaining(character) <= 0:
        raise InventoryFullError("Cannot unequip, inventory full")

    add_item_to_inventory(character, armor)
    character["equipped_armor"] = None
    character["equipped_armor_effect"] = None

    return armor

# ============================================================================
# SHOP SYSTEM
# ============================================================================

def purchase_item(character, item_id, item_data):
    """
    Buy an item
    """
    cost = item_data["cost"]

    if character["gold"] < cost:
        raise InsufficientResourcesError("Not enough gold")

    if get_inventory_space_remaining(character) <= 0:
        raise InventoryFullError("Inventory full")

    character["gold"] -= cost
    add_item_to_inventory(character, item_id)

    return True


def sell_item(character, item_id, item_data):
    """
    Sell an item
    """
    if not has_item(character, item_id):
        raise ItemNotFoundError(f"Item '{item_id}' not found")

    sell_price = item_data["cost"] // 2
    remove_item_from_inventory(character, item_id)

    character["gold"] += sell_price
    return sell_price

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_item_effect(effect_string):
    """
    "health:20" → ("health", 20)
    """
    stat, val = effect_string.split(":")
    return stat, int(val)


def apply_stat_effect(character, stat_name, value):
    """
    Apply stat
    """
    character[stat_name] += value

    # Cap health at max_health
    if stat_name == "health":
        if character["health"] > character["max_health"]:
            character["health"] = character["max_health"]


def display_inventory(character, item_data_dict):
    """
    Print inventory list with quantities
    """
    print("\n=== INVENTORY ===")

    counts = {}
    for item in character["inventory"]:
        counts[item] = counts.get(item, 0) + 1

    if not counts:
        print("Inventory is empty.")
        return

    for item_id, qty in counts.items():
        info = item_data_dict[item_id]
        print(f"{info['name']} (Type: {info['type']}) × {qty}")

    print("=================\n")
