"""
COMP 163 - Project 3: Quest Chronicles
Game Data Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This module handles loading and validating game data from text files.
"""

import os
from custom_exceptions import (
    InvalidDataFormatError,
    MissingDataFileError,
    CorruptedDataError
)

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

def load_quests(filename="data/quests.txt"):
    """
    Load quest data from file
    
    Expected format per quest (separated by blank lines):
    QUEST_ID: unique_quest_name
    TITLE: Quest Display Title
    DESCRIPTION: Quest description text
    REWARD_XP: 100
    REWARD_GOLD: 50
    REQUIRED_LEVEL: 1
    PREREQUISITE: previous_quest_id (or NONE)
    
    Returns: Dictionary of quests {quest_id: quest_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        raise MissingDataFileError(f"Quest file is not found: {filename}")
    except Exception:
        raise CorruptedDataError(f"Quest file is unreadable: {filename}")
    
    quest = {}
    current_block = []

    for line in lines:
        stripped = line.strip()
        if stripped == "":
            if current_block:
                quest_dict = parse_quest_block(current_block)
                validate_quest_data(quest_dict)
                quest[quest_dict['quest_id']] = quest_dict
                current_block = []
        else:
            current_block.append(stripped)
    
    if current_block:
        quest_dict = parse_quest_block(current_block)
        validate_quest_data(quest_dict)
        quest[quest_dict['quest_id']] = quest_dict

    return quest



def load_items(filename="data/items.txt"):
    """
    Load item data from file
    
    Expected format per item (separated by blank lines):
    ITEM_ID: unique_item_name
    NAME: Item Display Name
    TYPE: weapon|armor|consumable
    EFFECT: stat_name:value (e.g., strength:5 or health:20)
    COST: 100
    DESCRIPTION: Item description
    
    Returns: Dictionary of items {item_id: item_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        raise MissingDataFileError(f"Item data file is not found: {filename}")
    except Exception:
        raise CorruptedDataError(f"Item file is unreadable: {filename}")
    
    item = {}
    current_block = []

    for line in lines:
        stripped = line.strip()
        if stripped == "":
            if current_block:
                item_dict = parse_item_block(current_block)
                validate_item_data(item_dict)
                item[item_dict['item_id']] = item_dict
                current_block = []
        else:
            current_block.append(stripped)

    if current_block:
        item_dict = parse_item_block(current_block)
        validate_item_data(item_dict)
        item[item_dict['item_id']] = item_dict

    return item


def validate_quest_data(quest_dict):
    """
    Validate that quest dictionary has all required fields
    
    Required fields: quest_id, title, description, reward_xp, 
                    reward_gold, required_level, prerequisite
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields
    """
    required_fields = [
        "quest_id",
        "title",
        "description",
        "reward_xp",
        "reward_gold",
        "required_level",
        "prerequisite"
    ]
    #checking for required fields
    for field in required_fields:
        if field not in quest_dict:
            raise InvalidDataFormatError(f"Missing field in quest: {field}")
        
    numeric_fields = ["reward_xp", "reward_gold", "required_level"]

    for key in numeric_fields:
        if not isinstance(quest_dict[key], int):
            raise InvalidDataFormatError(f"Field {key} must be an integer")
    return True


def validate_item_data(item_dict):
    """
    Validate that item dictionary has all required fields
    
    Required fields: item_id, name, type, effect, cost, description
    Valid types: weapon, armor, consumable
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields or invalid type
    """
    required_fields = [
        "item_id",
        "name",
        "type",
        "effect",
        "cost",
        "description"
    ]
    for field in required_fields:
        if field not in item_dict:
            raise InvalidDataFormatError(f"Missing field in item: {field}")
        
        #Type must be weapon, armor or a consumable
    valid_types = {"weapon", "armor", "consumable"}

    if item_dict["type"] not in valid_types:
        raise InvalidDataFormatError(f"Invalid item type: {item_dict['type']}")
    
    #Cost must be a real integer
    if not isinstance(item_dict["cost"], int):
        raise InvalidDataFormatError("Item cost must be an integer")
    
    #Effect must be in the format stat_name:value
    if ":" not in item_dict["effect"]:
        raise InvalidDataFormatError("Item effect must be in format stat_name:value")
    return True
    # TODO: Implement validation


def create_default_data_files():
    """
    Create default data files if they don't exist
    This helps with initial setup and testing
    """
    #makes data directory if it doesn't exist
    if not os.path.exists("data"):
        os.makedirs("data")

    # Create default quests.txt
    if not os.path.exists("data/quests.txt"):
        try:
            with open("data/quests.txt", "w") as f:
                f.write(
"""QUEST_ID: slay_goblin
TITLE: Slay the Goblin
DESCRIPTION: A goblin threatens the village.
REWARD_XP: 100
REWARD_GOLD: 50
REQUIRED_LEVEL: 1
PREREQUISITE: NONE

"""
                )
        except Exception:
            raise CorruptedDataError("Unable to create quests.txt")

    # Create default items.txt
    if not os.path.exists("data/items.txt"):
        try:
            with open("data/items.txt", "w") as f:
                f.write(
"""ITEM_ID: iron_sword
NAME: Iron Sword
TYPE: weapon
EFFECT: strength:5
COST: 50
DESCRIPTION: Basic melee weapon.

"""
                )
        except Exception:
            raise CorruptedDataError("Unable to create items.txt")
    # TODO: Implement this function
    # Create data/ directory if it doesn't exist
    # Create default quests.txt and items.txt files
    # Handle any file permission errors appropriately

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_quest_block(lines):
    """
    Parse a block of lines into a quest dictionary
    
    Args:
        lines: List of strings representing one quest
    
    Returns: Dictionary with quest data
    Raises: InvalidDataFormatError if parsing fails
    """
    quest = {}

    for line in lines:
        if ":" not in line:
            raise InvalidDataFormatError(f"Quest line missing ':' seperator")
        
        key, value = line.split(":", 1)

        key = key.strip().lower()
        value = value.strip()

        quest[key] = value

    try:
        quest["reward_xp"] = int(quest["reward_xp"])
        quest["reward_gold"] = int(quest["reward_gold"])
        quest["required_level"] = int(quest["required_level"])
    except Exception:
        raise InvalidDataFormatError("Quest numeric field is invalid")
    return quest
    # TODO: Implement parsing logic
    # Split each line on ": " to get key-value pairs
    # Convert numeric strings to integers
    # Handle parsing errors gracefully
    pass

def parse_item_block(lines):
    """
    Parse a block of lines into an item dictionary
    
    Args:
        lines: List of strings representing one item
    
    Returns: Dictionary with item data
    Raises: InvalidDataFormatError if parsing fails
    """
    item = {}

    for line in lines:
        if ": " not in line:
            raise InvalidDataFormatError("Item line missing ': ' separator")

        key, value = line.split(": ", 1)

        key = key.strip().lower()
        value = value.strip()

        item[key] = value

    # Convert cost to int
    try:
        item["cost"] = int(item["cost"])
    except Exception:
        raise InvalidDataFormatError("Item cost must be an integer")

    return item

    # TODO: Implement parsing logic

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== GAME DATA MODULE TEST ===")
    
    # Test creating default files
    # create_default_data_files()
    
    # Test loading quests
    try:
         quests = load_quests()
         print(f"Loaded {len(quests)} quests")
    except MissingDataFileError:
         print("Quest file not found")
    except InvalidDataFormatError as e:
         print(f"Invalid quest format: {e}")
    
    # Test loading items
    try:
         items = load_items()
         print(f"Loaded {len(items)} items")
    except MissingDataFileError:
         print("Item file not found")
    except InvalidDataFormatError as e:
         print(f"Invalid item format: {e}")

