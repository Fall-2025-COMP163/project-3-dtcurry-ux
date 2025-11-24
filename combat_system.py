
"""
COMP 163 - Project 3: Quest Chronicles
Combat System Module

Name: [Darenell Curry]

AI Usage: [Document any AI assistance used]

Handles combat mechanics: enemy creation, battle flow, damage calculation,
special abilities, and combat utilities.
"""

import random
from custom_exceptions import (
    InvalidTargetError,
    CombatNotActiveError,
    CharacterDeadError,
    AbilityOnCooldownError
)

# ============================================================================
# ENEMY DEFINITIONS
# ============================================================================

def create_enemy(enemy_type):
    """
    Create an enemy based on type.

    Enemy types and stats:
    - goblin: health=50, strength=8, magic=2, xp_reward=25, gold_reward=10
    - orc: health=80, strength=12, magic=5, xp_reward=50, gold_reward=25
    - dragon: health=200, strength=25, magic=15, xp_reward=200, gold_reward=100

    Returns:
        Dictionary with enemy data: name, health, max_health, strength, magic,
        xp_reward, gold_reward.

    Raises:
        InvalidTargetError: If enemy_type is not recognized.
    """
    enemy_type = enemy_type.lower()  # Normalize input
    if enemy_type == "goblin":
        return {"name": "Goblin", "health": 50, "max_health": 50,
                "strength": 8, "magic": 2, "xp_reward": 25, "gold_reward": 10}
    elif enemy_type == "orc":
        return {"name": "Orc", "health": 80, "max_health": 80,
                "strength": 12, "magic": 5, "xp_reward": 50, "gold_reward": 25}
    elif enemy_type == "dragon":
        return {"name": "Dragon", "health": 200, "max_health": 200,
                "strength": 25, "magic": 15, "xp_reward": 200, "gold_reward": 100}
    else:
        raise InvalidTargetError(f"Unknown enemy type: {enemy_type}")


def get_random_enemy_for_level(character_level):
    """
    Select an enemy based on character level.

    Level ranges:
    - 1-2: Goblins
    - 3-5: Orcs
    - 6+: Dragons

    Returns:
        Enemy dictionary.
    """
    if character_level <= 2:
        return create_enemy("goblin")
    elif character_level <= 5:
        return create_enemy("orc")
    else:
        return create_enemy("dragon")

def display_battle_log(message):
    raise NotImplementedError

def get_victory_rewards(enemy):
    raise NotImplementedError

def display_combat_stats(character, enemy):
    raise NotImplementedError


# ============================================================================
# COMBAT SYSTEM
# ============================================================================

class SimpleBattle:
    """
    Simple turn-based combat system between a character and an enemy.
    """

    def __init__(self, character, enemy):
        """
        Initialize battle with character and enemy.
        """
        self.character = character
        self.enemy = enemy
        self.combat_active = True
        self.turn_count = 0

    def start_battle(self):
        """
        Start the combat loop.

        Returns:
            Dictionary with battle results:
            {'winner': 'player'|'enemy', 'xp_gained': int, 'gold_gained': int}

        Raises:
            CharacterDeadError: If character is already dead.
        """
        if self.character["health"] <= 0:
            raise CharacterDeadError("Character is dead and cannot fight.")

        display_battle_log("Battle begins!")
        display_combat_stats(self.character, self.enemy)

        # Loop until someone dies or player escapes
        while self.combat_active:
            self.turn_count += 1
            display_battle_log(f"--- Turn {self.turn_count} ---")

            # Player's turn
            self.player_turn()
            winner = self.check_battle_end()
            if winner:
                break

            # Enemy's turn
            self.enemy_turn()
            winner = self.check_battle_end()
            if winner:
                break

            display_combat_stats(self.character, self.enemy)

        # Determine result
        if winner == "player":
            rewards = get_victory_rewards(self.enemy)
            display_battle_log(f"You defeated {self.enemy['name']}!")
            return {"winner": "player", "xp_gained": rewards["xp"], "gold_gained": rewards["gold"]}
        elif winner == "enemy":
            display_battle_log("You were defeated...")
            return {"winner": "enemy", "xp_gained": 0, "gold_gained": 0}
        else:
            display_battle_log("You escaped!")
            return {"winner": "escaped", "xp_gained": 0, "gold_gained": 0}

    def player_turn(self):
        """
        Handle player's turn: choose action.
        """
        if not self.combat_active:
            raise CombatNotActiveError("Combat is not active.")

        print("\nYour turn! Choose an action:")
        print("1. Basic Attack")
        print("2. Special Ability")
        print("3. Try to Run")

        choice = input("Enter choice (1-3): ").strip()
        if choice == "1":
            dmg = self.calculate_damage(self.character, self.enemy)
            self.apply_damage(self.enemy, dmg)
            display_battle_log(f"You attack for {dmg} damage!")
        elif choice == "2":
            result = use_special_ability(self.character, self.enemy)
            display_battle_log(result)
        elif choice == "3":
            escaped = self.attempt_escape()
            if escaped:
                display_battle_log("You successfully escaped!")
            else:
                display_battle_log("Escape failed!")
        else:
            display_battle_log("Invalid choice! You lose your turn.")

    def enemy_turn(self):
        """
        Enemy attacks the player.
        """
        if not self.combat_active:
            raise CombatNotActiveError("Combat is not active.")

        dmg = self.calculate_damage(self.enemy, self.character)
        self.apply_damage(self.character, dmg)
        display_battle_log(f"{self.enemy['name']} attacks for {dmg} damage!")

    def calculate_damage(self, attacker, defender):
        """
        Damage formula:
        attacker['strength'] - (defender['strength'] // 4)
        Minimum damage: 1
        """
        dmg = attacker["strength"] - (defender["strength"] // 4)
        return dmg if dmg > 0 else 1

    def apply_damage(self, target, damage):
        """
        Apply damage to target without going below 0 HP.
        """
        target["health"] -= damage
        if target["health"] < 0:
            target["health"] = 0

    def check_battle_end(self):
        """
        Check if battle is over.
        Returns:
            'player' if enemy dead, 'enemy' if character dead, None if ongoing.
        """
        if self.enemy["health"] <= 0:
            self.combat_active = False
            return "player"
        elif self.character["health"] <= 0:
            self.combat_active = False
            return "enemy"
        return None

    def attempt_escape(self):
        """
        50% chance to escape.
        """
        success = random.random() < 0.5
        if success:
            self.combat_active = False
        return success


# ============================================================================
# SPECIAL ABILITIES
# ============================================================================

def use_special_ability(character, enemy):
    """
    Use class-specific ability.
    """
    cls = character["class"]
    if cls == "Warrior":
        return warrior_power_strike(character, enemy)
    elif cls == "Mage":
        return mage_fireball(character, enemy)
    elif cls == "Rogue":
        return rogue_critical_strike(character, enemy)
    elif cls == "Cleric":
        return cleric_heal(character)
    else:
        return "No special ability available."


def warrior_power_strike(character, enemy):
    dmg = character["strength"] * 2
    enemy["health"] -= dmg
    if enemy["health"] < 0:
        enemy["health"] = 0
    return f"Warrior uses Power Strike! Deals {dmg} damage."


def mage_fireball(character, enemy):
    dmg = character["magic"] * 2
    enemy["health"] -= dmg
    if enemy["health"] < 0:
        enemy["health"] = 0
    return f"Mage casts Fireball! Deals {dmg} damage."


def rogue_critical_strike(character, enemy):
    if random.random() < 0.5:
        dmg = character["strength"] * 3
        enemy["health"] -= dmg
        if enemy["health"] < 0:
            enemy["health"] = 0
        return f"Critical Strike! Deals {dmg} damage."
    else:
        return "Critical Strike missed!"

def reduce_cooldowns(character):
    """
    Reduce all cooldowns by 1 after each turn.
    """
    if "cooldowns" in character:
        for ability in character["cooldowns"]:
            if character["cooldowns"][ability] > 0:
                character["cooldowns"][ability] -= 1

def cleric_heal(character):
    heal_amount = 30
    missing = character["max_health"] - character["health"]
    if missing <= 0:
        return "Cleric is already at full health."
    

def use_special_ability(character, enemy):
    """
    Use character's class-specific special ability.
    Raises AbilityOnCooldownError if ability is still cooling down.
    """
    # Initialize cooldown dictionary if missing
    if "cooldowns" not in character:
        character["cooldowns"] = {}

    # Check cooldown for special ability
    if character["cooldowns"].get("special", 0) > 0:
        raise AbilityOnCooldownError("Special ability is on cooldown!")

    # Execute ability based on class
    cls = character["class"]
    if cls == "Warrior":
        result = warrior_power_strike(character, enemy)
    elif cls == "Mage":
        result = mage_fireball(character, enemy)
    elif cls == "Rogue":
        result = rogue_critical_strike(character, enemy)
    elif cls == "Cleric":
        result = cleric_heal(character)
    else:
        result = "No special ability available."

    # Set cooldown (e.g., 3 turns)
    character["cooldowns"]["special"] = 3
    return result


def reduce_cooldowns(character):
    """
    Reduce all cooldowns by 1 after each turn.
    """
    if "cooldowns" in character:
        for ability in character["cooldowns"]:
            if character["cooldowns"][ability] > 0:
                character["cooldowns"][ability] -= 1
    pass

def get_random_enemy_for_level(character_level):
    """
    Get an appropriate enemy for character's level
    
    Level 1-2: Goblins
    Level 3-5: Orcs
    Level 6+: Dragons
    
    Returns: Enemy dictionary
    """
    # TODO: Implement level-appropriate enemy selection
    # Use if/elif/else to select enemy type
    # Call create_enemy with appropriate type
    pass

# ============================================================================
# COMBAT SYSTEM
# ============================================================================

class SimpleBattle:
    """
    Simple turn-based combat system
    
    Manages combat between character and enemy
    """
    
    def __init__(self, character, enemy):
        """Initialize battle with character and enemy"""
        # TODO: Implement initialization
        # Store character and enemy
        # Set combat_active flag
        # Initialize turn counter
        pass
    
    def start_battle(self):
        """
        Start the combat loop
        
        Returns: Dictionary with battle results:
                {'winner': 'player'|'enemy', 'xp_gained': int, 'gold_gained': int}
        
        Raises: CharacterDeadError if character is already dead
        """
        # TODO: Implement battle loop
        # Check character isn't dead
        # Loop until someone dies
        # Award XP and gold if player wins
        pass
    
    def player_turn(self):
        """
        Handle player's turn
        
        Displays options:
        1. Basic Attack
        2. Special Ability (if available)
        3. Try to Run
        
        Raises: CombatNotActiveError if called outside of battle
        """
        # TODO: Implement player turn
        # Check combat is active
        # Display options
        # Get player choice
        # Execute chosen action
        pass
    
    def enemy_turn(self):
        """
        Handle enemy's turn - simple AI
        
        Enemy always attacks
        
        Raises: CombatNotActiveError if called outside of battle
        """
        # TODO: Implement enemy turn
        # Check combat is active
        # Calculate damage
        # Apply to character
        pass
    
    def calculate_damage(self, attacker, defender):
        """
        Calculate damage from attack
        
        Damage formula: attacker['strength'] - (defender['strength'] // 4)
        Minimum damage: 1
        
        Returns: Integer damage amount
        """
        # TODO: Implement damage calculation
        pass
    
    def apply_damage(self, target, damage):
        """
        Apply damage to a character or enemy
        
        Reduces health, prevents negative health
        """
        # TODO: Implement damage application
        pass
    
    def check_battle_end(self):
        """
        Check if battle is over
        
        Returns: 'player' if enemy dead, 'enemy' if character dead, None if ongoing
        """
        # TODO: Implement battle end check
        pass
    
    def attempt_escape(self):
        """
        Try to escape from battle
        
        50% success chance
        
        Returns: True if escaped, False if failed
        """
        # TODO: Implement escape attempt
        # Use random number or simple calculation
        # If successful, set combat_active to False
        pass

# ============================================================================
# SPECIAL ABILITIES
# ============================================================================

def use_special_ability(character, enemy):
    """
    Use character's class-specific special ability
    
    Example abilities by class:
    - Warrior: Power Strike (2x strength damage)
    - Mage: Fireball (2x magic damage)
    - Rogue: Critical Strike (3x strength damage, 50% chance)
    - Cleric: Heal (restore 30 health)
    
    Returns: String describing what happened
    Raises: AbilityOnCooldownError if ability was used recently
    """
    # TODO: Implement special abilities
    # Check character class
    # Execute appropriate ability
    # Track cooldowns (optional advanced feature)
    pass

def warrior_power_strike(character, enemy):
    """Warrior special ability"""
    # TODO: Implement power strike
    # Double strength damage
    pass

def mage_fireball(character, enemy):
    """Mage special ability"""
    # TODO: Implement fireball
    # Double magic damage
    pass

def rogue_critical_strike(character, enemy):
    """Rogue special ability"""
    # TODO: Implement critical strike
    # 50% chance for triple damage
    pass

def cleric_heal(character):
    """Cleric special ability"""
    # TODO: Implement healing
    # Restore 30 HP (not exceeding max_health)
    pass

# ============================================================================
# COMBAT UTILITIES
# ============================================================================

def can_character_fight(character):
    """
    Check if character is in condition to fight
    
    Returns: True if health > 0 and not in battle
    """
    # TODO: Implement fight check
    pass

def get_victory_rewards(enemy):
    """
    Calculate rewards for defeating enemy
    
    Returns: Dictionary with 'xp' and 'gold'
    """
    # TODO: Implement reward calculation
    pass

def display_combat_stats(character, enemy):
    """
    Display current combat status
    
    Shows both character and enemy health/stats
    """
    # TODO: Implement status display
    print(f"\n{character['name']}: HP={character['health']}/{character['max_health']}")
    print(f"{enemy['name']}: HP={enemy['health']}/{enemy['max_health']}")
    pass

def display_battle_log(message):
    """
    Display a formatted battle message
    """
    # TODO: Implement battle log display
    print(f">>> {message}")
    pass

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== COMBAT SYSTEM TEST ===")
    
    # Test enemy creation
    # try:
    #     goblin = create_enemy("goblin")
    #     print(f"Created {goblin['name']}")
    # except InvalidTargetError as e:
    #     print(f"Invalid enemy: {e}")
    
    # Test battle
    # test_char = {
    #     'name': 'Hero',
    #     'class': 'Warrior',
    #     'health': 120,
    #     'max_health': 120,
    #     'strength': 15,
    #     'magic': 5
    # }
    #
    # battle = SimpleBattle(test_char, goblin)
    # try:
    #     result = battle.start_battle()
    #     print(f"Battle result: {result}")
    # except CharacterDeadError:
    #     print("Character is dead!")

