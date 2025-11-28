"""
COMP 163 - Project 3: Quest Chronicles
Combat System Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

Handles combat mechanics
"""

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
    Create an enemy based on type
    
    Example enemy types and stats:
    - goblin: health=50, strength=8, magic=2, xp_reward=25, gold_reward=10
    - orc: health=80, strength=12, magic=5, xp_reward=50, gold_reward=25
    - dragon: health=200, strength=25, magic=15, xp_reward=200, gold_reward=100
    
    Returns: Enemy dictionary
    Raises: InvalidTargetError if enemy_type not recognized
    """
    enemy_types = {
        "goblin": {
            "name": "Goblin",
            "health": 50,
            "strength": 8,
            "magic": 2,
            "xp_reward": 25,
            "gold_reward": 10
        },
        "orc": {
            "name": "Orc",
            "health": 80,
            "strength": 12,
            "magic": 5,
            "xp_reward": 50,
            "gold_reward": 25
        },
        "dragon": {
            "name": "Dragon",
            "health": 200,
            "strength": 25,
            "magic": 15,
            "xp_reward": 200,
            "gold_reward": 100
        }
    }
    if enemy_type not in enemy_types:
        raise InvalidTargetError(f"Unknown enemy type: {enemy_type}")
    
    base = enemy_types[enemy_type]

    enemy = {
        "name": base["name"],
        "health": base["health"],
        "max_health": base["health"],
        "strength": base["strength"],
        "magic": base["magic"],
        "xp_reward": base["xp_reward"],
        "gold_reward": base["gold_reward"]
    }
    return enemy
    # TODO: Implement enemy creation
    # Return dictionary with: name, health, max_health, strength, magic, xp_reward, gold_reward

def get_random_enemy_for_level(character_level):
    """
    Get an appropriate enemy for character's level
    
    Level 1-2: Goblins
    Level 3-5: Orcs
    Level 6+: Dragons
    
    Returns: Enemy dictionary
    """
    if character_level <= 2:
        enemy_type = "goblin"
    elif character_level <= 5:
        enemy_type = "orc"
    else:
        enemy_type = "dragon"
    return create_enemy(enemy_type)
    # TODO: Implement level-appropriate enemy selection
    # Use if/elif/else to select enemy type
    # Call create_enemy with appropriate type

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
        self.character = character
        self.enemy = enemy

        self.combat_active = True

        self.turn_number = 1
        # TODO: Implement initialization
        # Store character and enemy
        # Set combat_active flag
        # Initialize turn counter
    
    def start_battle(self):
        """
        Start the combat loop
        
        Returns: Dictionary with battle results:
                {'winner': 'player'|'enemy', 'xp_gained': int, 'gold_gained': int}
        
        Raises: CharacterDeadError if character is already dead
        """
        #cant start battle if character is dead
        if self.character["health"] <= 0:
            raise CharacterDeadError("Character is dead and cannot fight")
        
        #loop until battle ends
        while self.combat_active:

            self.player_turn()
            result = self.check_battle_end()
            if result:
                break

            #enemy turn
            self.enemy_turn()
            result = self.check_battle_end()
            if result:
                break

            #increment turn counter
            self.turn_number += 1

        #determine winner and rewards after loop ends
        if result == "player":
            rewards = get_victory_rewards(self.enemy)

            #Award XP and gold to character
            #XP leveling happens in character manager
            self.character["experience"] += rewards["xp"]
            self.character["gold"] += rewards["gold"]

            return {
                'winner': 'player',
                'xp_gained': rewards["xp"],
                'gold_gained': rewards["gold"]
            }
        
        elif result == "enemy":
            return {
                'winner': 'enemy',
                'xp_gained': 0,
                'gold_gained': 0
            }
        
        else:
            #escape means no winner
            return {
                'winner': 'none',
                'xp_gained': 0,
                'gold_gained': 0
            }
        
        # TODO: Implement battle loop
        # Check character isn't dead
        # Loop until someone dies
        # Award XP and gold if player wins
    
    def player_turn(self):
        """
        Handle player's turn
        
        Displays options:
        1. Basic Attack
        2. Special Ability (if available)
        3. Try to Run
        
        Raises: CombatNotActiveError if called outside of battle
        """
        if not self.combat_active:
            raise CombatNotActiveError("Combat is not active")
        
        display_combat_stats(self.character, self.enemy)

        #Show Options
        print("\nYour Turn! Choose an action:")
        print("1. Basic Attack")
        print("2. Special Ability")
        print("3. Try to Run")

        choice = input("Enter choice (1-3): ").strip()

        #Basic Attack
        if choice == "1":
            damage = self.calculate_damage(self.character, self.enemy)
            self.apply_damage(self.enemy, damage)
            display_battle_log(f"You attack the {self.enemy['name']} for {damage} damage!")

        #Special Ability
        elif choice == "2":
            result_text = use_special_ability(self.character, self.enemy)
            display_battle_log(result_text)

        #Try to Run
        elif choice == "3":
            escaped = self.attempt_escape()
            if escaped:
                display_battle_log("You successfully escaped the battle!")
            else:
                display_battle_log("Escape failed! The battle continues.")
                return  # End turn if escape fails
        else:
            display_battle_log("Invalid choice! You lose your turn.")


        # TODO: Implement player turn
        # Check combat is active
        # Display options
        # Get player choice
        # Execute chosen action
    
    def enemy_turn(self):
        """
        Handle enemy's turn - simple AI
        
        Enemy always attacks
        
        Raises: CombatNotActiveError if called outside of battle
        """
        if not self.combat_active:
            raise CombatNotActiveError("Combat is not active")
        
        #enemy attacks player
        damage = self.calculate_damage(self.enemy, self.character)
        self.apply_damage(self.character, damage)

        #log attack
        display_battle_log(f"The {self.enemy['name']} attacks you for {damage} damage!")
        
        # TODO: Implement enemy turn
        # Check combat is active
        # Calculate damage
        # Apply to character
        
    
    def calculate_damage(self, attacker, defender):
        """
        Calculate damage from attack
        
        Damage formula: attacker['strength'] - (defender['strength'] // 4)
        Minimum damage: 1
        
        Returns: Integer damage amount
        """
        damage = attacker["strength"] - (defender["strength"] // 4)

        #ensure minimum damage of 1
        if damage < 1:
            damage = 1

        return damage
        # TODO: Implement damage calculation
    
    def apply_damage(self, target, damage):
        """
        Apply damage to a character or enemy
        
        Reduces health, prevents negative health
        """
        #reduce health by damage
        target["health"] -= damage

        #prevent negative health
        if target["health"] < 0:
            target["health"] = 0
        # TODO: Implement damage application
    
    def check_battle_end(self):
        """
        Check if battle is over
        
        Returns: 'player' if enemy dead, 'enemy' if character dead, None if ongoing
        """
        #enemy dead means player wins
        if self.enemy["health"] <= 0:
            self.combat_active = False
            return "player"
        
        #character dead means enemy wins
        if self.character["health"] <= 0:
            self.combat_active = False
            return "enemy"
        
        #battle ongoing
        return None
        
        # TODO: Implement battle end check
import random
def attempt_escape(self):
        """
        Try to escape from battle
        
        50% success chance
        
        Returns: True if escaped, False if failed
        """
        #random chance to escape 0 or 1
        success = random.radint(0,1)
        #escape successful ends battle
        if success == 1:
            self.combat_active = False
            return True
        
        #escape failed
        return False

        # TODO: Implement escape attempt
        # Use random number or simple calculation
        # If successful, set combat_active to False


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
    class_type = character["class"]

    if class_type == "Warrior":
        return warrior_power_strike(character, enemy)

    elif class_type == "Mage":
        return mage_fireball(character, enemy)

    elif class_type == "Rogue":
        return rogue_critical_strike(character, enemy)

    elif class_type == "Cleric":
        return cleric_heal(character)

    else:
        raise InvalidTargetError("Unknown character class for ability.")
    # TODO: Implement special abilities
    # Check character class
    # Execute appropriate ability
    # Track cooldowns (optional advanced feature)

def warrior_power_strike(character, enemy):
    """Warrior special ability"""
    #regular damage calculation
    base_damage = character["strength"] - (enemy["strength"] // 4)

    #minimum damage of 1
    if base_damage < 1:
        base_damage = 1

    #double damage for power strike
    final_damage = base_damage * 2

    #apply damage to enemy
    enemy["health"] -= final_damage
    if enemy["health"] < 0:
        enemy["health"] = 0
    return f"You use Power Strike and deal {final_damage} damage to the {enemy['name']}!"


    # TODO: Implement power strike
    # Double strength damage
    

def mage_fireball(character, enemy):
    """Mage special ability"""

    #regular magic damage calculation
    base_damage = character["magic"]

    #fireball doubles magic damage
    final_damage = base_damage * 2

    #apply damage to enemy
    enemy["health"] -= final_damage
    if enemy["health"] < 0:
        enemy["health"] = 0
    return f"You cast Fireball and deal {final_damage} magic damage to the {enemy['name']}!"

    # TODO: Implement fireball
    # Double magic damage
    

def rogue_critical_strike(character, enemy):
    """Rogue special ability"""
        # Calculate base damage (same formula as normal attack)
    base_damage = character["strength"] - (enemy["strength"] // 4)

    if base_damage < 1:
        base_damage = 1

    # 50% chance for a critical hit
    crit = random.randint(0, 1)  # 0 = normal, 1 = critical

    if crit == 1:
        final_damage = base_damage * 3
        crit_text = "Critical Strike!"
    else:
        final_damage = base_damage
        crit_text = "You strike swiftly."

    # Apply damage
    enemy["health"] -= final_damage
    if enemy["health"] < 0:
        enemy["health"] = 0

    return f"{crit_text} You dealt {final_damage} damage!"
    # TODO: Implement critical strike
    # 50% chance for triple damage

def cleric_heal(character):
    """Cleric special ability"""
    heal_amount = 30

    # Calculate how much healing can actually be applied
    max_hp = character["max_health"]
    current_hp = character["health"]

    new_hp = current_hp + heal_amount

    # Cap at max health
    if new_hp > max_hp:
        new_hp = max_hp

    actual_healed = new_hp - current_hp

    # Apply healing
    character["health"] = new_hp

    return f"You pray for divine aid and heal {actual_healed} HP!"
    # TODO: Implement healing
    # Restore 30 HP (not exceeding max_health)

# ============================================================================
# COMBAT UTILITIES
# ============================================================================

def can_character_fight(character):
    """
    Check if character is in condition to fight
    
    Returns: True if health > 0 and not in battle
    """
    return character["health"] > 0
    # TODO: Implement fight check

def get_victory_rewards(enemy):
    """
    Calculate rewards for defeating enemy
    
    Returns: Dictionary with 'xp' and 'gold'
    """
    return {
        'xp': enemy['xp_reward'],
        'gold': enemy['gold_reward']
    }
    # TODO: Implement reward calculation

def display_combat_stats(character, enemy):
    """
    Display current combat status
    
    Shows both character and enemy health/stats
    """
    print(f"\n{character['name']}: HP={character['health']}/{character['max_health']}")
    print(f"{enemy['name']}: HP={enemy['health']}/{enemy['max_health']}")

def display_battle_log(message):
    """
    Display a formatted battle message
    """
    print(f">>> {message}")

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== COMBAT SYSTEM TEST ===")
    
    #Test enemy creation
    try:
        goblin = create_enemy("goblin")
        print(f"Created {goblin['name']}")
    except InvalidTargetError as e:
        print(f"Invalid enemy: {e}")
    
    #Test battle
    test_char = {
        'name': 'Hero',
        'class': 'Warrior',
        'health': 120,
        'max_health': 120,
        'strength': 15,
        'magic': 5
    }
    
    battle = SimpleBattle(test_char, goblin)
    try:
        result = battle.start_battle()
        print(f"Battle result: {result}")
    except CharacterDeadError:
        print("Character is dead!")

