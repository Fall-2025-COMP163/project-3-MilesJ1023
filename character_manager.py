"""
COMP 163 - Project 3: Quest Chronicles
Character Manager Module - Starter Code

Name: Miles Johnson

AI Usage: [Document any AI assistance used]

This module handles character creation, loading, and saving.
"""

import os
from custom_exceptions import (
    InvalidCharacterClassError,
    CharacterNotFoundError,
    SaveFileCorruptedError,
    InvalidSaveDataError,
    CharacterDeadError
)

# ============================================================================
# CHARACTER MANAGEMENT FUNCTIONS
# ============================================================================

def create_character(name, character_class):
    """
    Create a new character with stats based on class
    
    Valid classes: Warrior, Mage, Rogue, Cleric
    
    Returns: Dictionary with character data including:
            - name, class, level, health, max_health, strength, magic
            - experience, gold, inventory, active_quests, completed_quests
    
    Raises: InvalidCharacterClassError if class is not valid
    """
    #user character classes
    valid_classes = {
        "Warrior": {"health": 120, "strength": 15, "magic": 5},
        "Mage": {"health": 80, "strength": 8, "magic": 20},
        "Rogue": {"health": 90, "strength": 12, "magic": 10},
        "Cleric": {"health": 100, "strength": 10, "magic": 15}
    }
    #prevents user from choosing invalid class
    if character_class not in valid_classes:
        raise InvalidCharacterClassError(f"Invalid class: {character_class}")
    
    #Gets the base stats for the chosen class
    base_stats = valid_classes[character_class]

# Creates the character dictionary with initial stats
    character = {
        "name": name,
        "class": character_class,
        "level": 1,
        "health": base_stats["health"],
        "max_health": base_stats["health"],
        "strength": base_stats["strength"],
        "magic": base_stats["magic"],
        "experience": 0,
        "gold": 100,
        "inventory": [],
        "active_quests": [],
        "completed_quests": []
    }

    return character



def save_character(character, save_directory="data/save_games"):
    """
    Save character to file
    
    Filename format: {character_name}_save.txt
    
    File format:
    NAME: character_name
    CLASS: class_name
    LEVEL: 1
    HEALTH: 120
    MAX_HEALTH: 120
    STRENGTH: 15
    MAGIC: 5
    EXPERIENCE: 0
    GOLD: 100
    INVENTORY: item1,item2,item3
    ACTIVE_QUESTS: quest1,quest2
    COMPLETED_QUESTS: quest1,quest2
    
    Returns: True if successful
    Raises: PermissionError, IOError (let them propagate or handle)
    """
    #creates save directory if it doesn't exist
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

#builds the filename and path
    filename = f"{character['name']}_save.txt"
    file_path = os.path.join(save_directory, filename)

    try:
        with open(file_path, "w") as file:
            file.write(f"NAME: {character['name']}\n")
            file.write(f"CLASS: {character['class']}\n")
            file.write(f"LEVEL: {character['level']}\n")
            file.write(f"HEALTH: {character['health']}\n")
            file.write(f"MAX_HEALTH: {character['max_health']}\n")
            file.write(f"STRENGTH: {character['strength']}\n")
            file.write(f"MAGIC: {character['magic']}\n")
            file.write(f"EXPERIENCE: {character['experience']}\n")
            file.write(f"GOLD: {character['gold']}\n")

            # Joins inventory list into comma-separated string
            inventory_str = ",".join(character['inventory'])
            file.write(f"INVENTORY: {inventory_str}\n")

            # Joins active quests list into comma-separated string
            active_quests_str = ",".join(character['active_quests'])
            file.write(f"ACTIVE_QUESTS: {active_quests_str}\n")

            # Joins completed quests list into comma-separated string
            completed_quests_str = ",".join(character['completed_quests'])
            file.write(f"COMPLETED_QUESTS: {completed_quests_str}\n")
        return True
    
    #handles file and IO errors
    except Exception as e:
        raise SaveFileCorruptedError(f"Error saving character: {e}")
    # TODO: Implement save functionality
    # Create save_directory if it doesn't exist
    # Handle any file I/O errors appropriately
    # Lists should be saved as comma-separated values

def load_character(character_name, save_directory="data/save_games"):
    """
    Load character from save file
    
    Args:
        character_name: Name of character to load
        save_directory: Directory containing save files
    
    Returns: Character dictionary
    Raises: 
        CharacterNotFoundError if save file doesn't exist
        SaveFileCorruptedError if file exists but can't be read
        InvalidSaveDataError if data format is wrong
    """
        # Build file path
    filename = f"{character_name}_save.txt"
    file_path = os.path.join(save_directory, filename)

    #Check if file exists
    if not os.path.exists(file_path):
        raise CharacterNotFoundError(f"No save file found for {character_name}")

    #Try to read the file
    try:
        with open(file_path, "r") as f:
            lines = f.readlines()
    except Exception as e:
        raise SaveFileCorruptedError(f"Could not read save file: {e}")

    character = {}

    #Parse each line into key/value pairs
    try:
        for line in lines:
            line = line.strip()

            if line == "":
                continue

            if ": " not in line:
                raise InvalidSaveDataError("Save file line missing ':' separator")

            key, value = line.strip().split(": ", 1)
            key = key.lower()

            #Convert empty values to empty lists later
            character[key] = value.strip()

        #Convert numeric fields back to ints
        character["level"] = int(character["level"])
        character["health"] = int(character["health"])
        character["max_health"] = int(character["max_health"])
        character["strength"] = int(character["strength"])
        character["magic"] = int(character["magic"])
        character["experience"] = int(character["experience"])
        character["gold"] = int(character["gold"])

        #Convert CSV lists back to Python lists
        def parse_list(value):
            return [] if value == "" else value.split(",")

        character["inventory"] = parse_list(character["inventory"])
        character["active_quests"] = parse_list(character["active_quests"])
        character["completed_quests"] = parse_list(character["completed_quests"])

    except Exception:
        raise InvalidSaveDataError("Save file has invalid data")

    return character

    # TODO: Implement load functionality
    # Check if file exists → CharacterNotFoundError
    # Try to read file → SaveFileCorruptedError
    # Validate data format → InvalidSaveDataError
    # Parse comma-separated lists back into Python lists

def list_saved_characters(save_directory="data/save_games"):
    """
    Get list of all saved character names
    
    Returns: List of character names (without _save.txt extension)
    """
#If directory doesn't exist, no saved characters
    if not os.path.exists(save_directory):
        return []

    characters = []

#Loop through all files in directory
    for filename in os.listdir(save_directory):

#Only include files that end with _save.txt
        if filename.endswith("_save.txt"):
            # Remove the suffix to get just the name
            character_name = filename.replace("_save.txt", "")
            characters.append(character_name)

    return characters

    # TODO: Implement this function
    # Return empty list if directory doesn't exist
    # Extract character names from filenames

def delete_character(character_name, save_directory="data/save_games"):
    """
    Delete a character's save file
    
    Returns: True if deleted successfully
    Raises: CharacterNotFoundError if character doesn't exist
    """
#Build the save file path
    filename = f"{character_name}_save.txt"
    file_path = os.path.join(save_directory, filename)

#Check if file exists
    if not os.path.exists(file_path):
        raise CharacterNotFoundError(f"No save file found for {character_name}")

    try:
        os.remove(file_path)
        return True

    except Exception:
#Rare: file exists but cannot be deleted (permissions etc.)
        raise SaveFileCorruptedError(f"Could not delete save file for {character_name}")
    # TODO: Implement character deletion
    # Verify file exists before attempting deletion

# ============================================================================
# CHARACTER OPERATIONS
# ============================================================================

def gain_experience(character, xp_amount):
    """
    Add experience to character and handle level ups
    
    Level up formula: level_up_xp = current_level * 100
    Example when leveling up:
    - Increase level by 1
    - Increase max_health by 10
    - Increase strength by 2
    - Increase magic by 2
    - Restore health to max_health
    
    Raises: CharacterDeadError if character health is 0
    """
#Check if character is dead
    if character["health"] <= 0:
        raise CharacterDeadError("Cannot gain XP while dead.")

#Add XP
    character["experience"] += xp_amount

#Continue leveling up as long as XP meets requirement
    while True:
        required_xp = character["level"] * 100

#Not enough XP means stop
        if character["experience"] < required_xp:
            break

#Use up the XP required for level-up
        character["experience"] -= required_xp

#Level up
        character["level"] += 1
        character["max_health"] += 10
        character["strength"] += 2
        character["magic"] += 2

#Restores health on level up
        character["health"] = character["max_health"]

    return character

    # TODO: Implement experience gain and leveling
    # Check if character is dead first
    # Add experience
    # Check for level up (can level up multiple times)
    # Update stats on level up


def add_gold(character, amount):
    """
    Add gold to character's inventory
    
    Args:
        character: Character dictionary
        amount: Amount of gold to add (can be negative for spending)
    
    Returns: New gold total
    Raises: ValueError if result would be negative
    """
#Calculate new gold amount
    new_total = character["gold"] + amount

#Don't allow negative gold
    if new_total < 0:
        raise ValueError("Gold cannot go below zero #broke.")

#Update gold
    character["gold"] = new_total

    return new_total

    # TODO: Implement gold management
    # Check that result won't be negative
    # Update character's gold


def heal_character(character, amount):
    """
    Heal character by specified amount
    
    Health cannot exceed max_health
    
    Returns: Actual amount healed
    """
    # Current health
    current = character["health"]
    max_hp = character["max_health"]

# If healing would exceed max, cap it
    new_health = min(current + amount, max_hp)

# Amount actually healed
    healed_amount = new_health - current

# Update character's health
    character["health"] = new_health

    return healed_amount

    # TODO: Implement healing
    # Calculate actual healing (don't exceed max_health)
    # Update character health


def is_character_dead(character):
    """
    Check if character's health is 0 or below
    
    Returns: True if dead, False if alive
    """
    return character["health"] <= 0

    # TODO: Implement death check

def revive_character(character):
    """
    Revive a dead character with 50% health
    
    Returns: True if revived
    """
#If not dead, nothing to do
    if character["health"] > 0:
        return False

#Revive at half max health
    character["health"] = character["max_health"] // 2

    return True

    # TODO: Implement revival
    # Restore health to half of max_health

# ============================================================================
# VALIDATION
# ============================================================================

def validate_character_data(character):
    """
    Validate that character dictionary has all required fields
    
    Required fields: name, class, level, health, max_health, 
                    strength, magic, experience, gold, inventory,
                    active_quests, completed_quests
    
    Returns: True if valid
    Raises: InvalidSaveDataError if missing fields or invalid types
    """
    required_fields = [
        "name", "class", "level", "health", "max_health",
        "strength", "magic", "experience", "gold",
        "inventory", "active_quests", "completed_quests"
    ]

#Check all required keys exist
    for key in required_fields:
        if key not in character:
            raise InvalidSaveDataError(f"Missing field: {key}")

#Check numerical fields
    numeric_fields = [
        "level", "health", "max_health",
        "strength", "magic", "experience", "gold"
    ]

    for key in numeric_fields:
        if not isinstance(character[key], int):
            raise InvalidSaveDataError(f"Invalid numeric value for {key}")

#Check list fields
    list_fields = ["inventory", "active_quests", "completed_quests"]

    for key in list_fields:
        if not isinstance(character[key], list):
            raise InvalidSaveDataError(f"{key} must be a list")

    return True

    # TODO: Implement validation
    # Check all required keys exist
    # Check that numeric values are numbers
    # Check that lists are actually lists

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== CHARACTER MANAGER TEST ===")
    
    # Test character creation
    # try:
    #     char = create_character("TestHero", "Warrior")
    #     print(f"Created: {char['name']} the {char['class']}")
    #     print(f"Stats: HP={char['health']}, STR={char['strength']}, MAG={char['magic']}")
    # except InvalidCharacterClassError as e:
    #     print(f"Invalid class: {e}")
    
    # Test saving
    # try:
    #     save_character(char)
    #     print("Character saved successfully")
    # except Exception as e:
    #     print(f"Save error: {e}")
    
    # Test loading
    # try:
    #     loaded = load_character("TestHero")
    #     print(f"Loaded: {loaded['name']}")
    # except CharacterNotFoundError:
    #     print("Character not found")
    # except SaveFileCorruptedError:
    #     print("Save file corrupted")

