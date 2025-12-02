"""
COMP 163 - Project 3: Quest Chronicles
Custom Exception Definitions

Name: Darenell Curry
AI Usage: Some AI guidance was used to suggest hierarchy and naming conventions.
"""

# ============================================================================ 
# BASE GAME EXCEPTIONS
# ============================================================================
class GameError(Exception):
    """Base exception for all game-related errors."""
    pass

class DataError(GameError):
    """Base exception for data-related errors (loading, saving)."""
    pass

class CharacterError(GameError):
    """Base exception for character-related errors."""
    pass

class CombatError(GameError):
    """Base exception for combat-related errors."""
    pass

class QuestError(GameError):
    """Base exception for quest-related errors."""
    pass

class InventoryError(GameError):
    """Base exception for inventory-related errors."""
    pass

# ============================================================================ 
# SPECIFIC EXCEPTIONS
# ============================================================================

# Data Loading Exceptions
class InvalidDataFormatError(DataError):
    """Raised when game data is formatted incorrectly."""
    pass

class MissingDataFileError(DataError):
    """Raised when a required data file is missing."""
    pass

class CorruptedDataError(DataError):
    """Raised when a data file is corrupted."""
    pass

# Character Exceptions
class InvalidCharacterClassError(CharacterError):
    """Raised when a player selects a non-existent class."""
    pass

class CharacterNotFoundError(CharacterError):
    """Raised when a saved character cannot be found."""
    pass

class CharacterDeadError(CharacterError):
    """Raised when trying to perform actions with a dead character."""
    pass

class InsufficientLevelError(CharacterError):
    """Raised when a character tries to accept a quest or item above their level."""
    pass

# Combat
