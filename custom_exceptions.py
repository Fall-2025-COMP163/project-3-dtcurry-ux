
"""
COMP 163 - Project 3: Quest Chronicles
Custom Exception Definitions

Name: [Darenell Curry]
AI Usage: [Document any AI assistance used]
This module defines all custom exceptions used throughout the game.
Exceptions are grouped into categories for clarity and easier error handling.
"""

# ============================================================================
# BASE GAME EXCEPTIONS
# ============================================================================
# These base classes allow us to organize errors by category.
# For example, all combat-related errors inherit from CombatError,
# making it easy to catch them together if needed.

class GameError(Exception):
    """Base exception for all game-related errors."""
    pass

class DataError(GameError):
    """Base exception for data-related errors (loading, saving)."""
    pass

class CharacterError(GameError):
    """Base exception for character-related errors (stats, actions)."""
    pass

class CombatError(GameError):
    """Base exception for combat-related errors (battle flow)."""
    pass

class QuestError(GameError):
    """Base exception for quest-related errors."""
    pass

class InventoryError(GameError):
    """Base exception for inventory-related errors."""
    pass

class InsufficientFundsError(InventoryError):
    """Raised when player doesn't have enough gold."""
    pass
# ============================================================================
# SPECIFIC EXCEPTIONS
# ============================================================================
# Each specific exception inherits from its category base class.
# This makes error handling flexible and organized.

# -------------------- Data Loading Exceptions --------------------
class InvalidDataFormatError(DataError):
    """Raised when a data file has incorrect format."""
    pass

class MissingDataFileError(DataError):
    """Raised when a required data file is not found."""
    pass

class CorruptedDataError(DataError):
    """Raised when a data file is corrupted or unreadable."""
    pass

# -------------------- Character Exceptions --------------------
class InvalidCharacterClassError(CharacterError):
    """Raised when an invalid character class is specified."""
    pass

class CharacterNotFoundError(CharacterError):
    """Raised when trying to load a character that doesn't exist."""
    pass

class CharacterDeadError(CharacterError):
    """Raised when trying to perform actions with a dead character."""
    pass

class InsufficientLevelError(CharacterError):
    """Raised when character level is too low for an action."""
    pass

# -------------------- Combat Exceptions --------------------
class InvalidTargetError(CombatError):
    """Raised when trying to target an invalid enemy."""
    pass

class CombatNotActiveError(CombatError):
    """Raised when trying to perform combat actions outside of battle."""
    pass

class AbilityOnCooldownError(CombatError):
    """Raised when trying to use an ability that's on cooldown."""
    pass

# -------------------- Quest Exceptions --------------------
class QuestNotFoundError(QuestError):
    """Raised when trying to access a quest that doesn't exist."""
    pass

class QuestRequirementsNotMetError(QuestError):
    """Raised when trying to start a quest without meeting requirements."""
    pass

class QuestAlreadyCompletedError(QuestError):
    """Raised when trying to accept an already completed quest."""
    pass

class QuestNotActiveError(QuestError):
    """Raised when trying to complete a quest that isn't active."""
    pass

# -------------------- Inventory Exceptions --------------------
class InventoryFullError(InventoryError):
    """Raised when trying to add items to a full inventory."""
    pass

class ItemNotFoundError(InventoryError):
    """Raised when trying to use an item that doesn't exist."""
    pass

class InsufficientResourcesError(InventoryError):
    """Raised when player doesn't have enough gold or items."""
    pass

class InvalidItemTypeError(InventoryError):
    """Raised when item type is not recognized."""
    pass

# -------------------- Save/Load Exceptions --------------------
class SaveFileCorruptedError(GameError):
    """Raised when save file cannot be loaded due to corruption."""
    pass

class InvalidSaveDataError(GameError):
    """Raised when save file contains invalid data."""
    pass

# ============================================================================
# Example Usage (for beginners)
# ============================================================================
# try:
#     raise InvalidCharacterClassError("Class 'Ninja' is not valid.")
# except InvalidCharacterClassError as e:
#     print(f"Error: {e}")
