"""
COMP 163 - Project 3: Quest Chronicles
Inventory System Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This module handles inventory management, item usage, and equipment.
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
    
    Args:
        character: Character dictionary
        item_id: Unique item identifier
    
    Returns: True if added successfully
    Raises: InventoryFullError if inventory is at max capacity
    """
    inventory = character["inventory"]

    #Check inventory capacity
    if len(inventory) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory is full")
    
    # add item
    inventory.append(item_id)
    return True

    # TODO: Implement adding items
    # Check if inventory is full (>= MAX_INVENTORY_SIZE)
    # Add item_id to character['inventory'] list

def remove_item_from_inventory(character, item_id):
    """
    Remove an item from character's inventory
    
    Args:
        character: Character dictionary
        item_id: Item to remove
    
    Returns: True if removed successfully
    Raises: ItemNotFoundError if item not in inventory
    """
    inventory = character["inventory"]

    # Check if item exists
    if item_id not in inventory:
        raise ItemNotFoundError(f"Item {item_id} not found in inventory")
    
    # Remove item only one though
    inventory.remove(item_id)
    return True

    # TODO: Implement item removal
    # Check if item exists in inventory
    # Remove item from list

def has_item(character, item_id):
    """
    Check if character has a specific item
    
    Returns: True if item in inventory, False otherwise
    """
    #check if item exists in inventory
    return item_id in character["inventory"]

    # TODO: Implement item check

def count_item(character, item_id):
    """
    Count how many of a specific item the character has
    
    Returns: Integer count of item
    """
    #count occurrences of item_id in inventory
    return character["inventory"].count(item_id)

    # TODO: Implement item counting
    # Use list.count() method

def get_inventory_space_remaining(character):
    """
    Calculate how many more items can fit in inventory
    
    Returns: Integer representing available slots
    """
    return MAX_INVENTORY_SIZE - len(character["inventory"])
    # TODO: Implement space calculation

def clear_inventory(character):
    """
    Remove all items from inventory
    
    Returns: List of removed items
    """
    #copy current inventory
    removed_items = character["inventory"][:]
    #clears inventory
    character["inventory"].clear()
    return removed_items
    # TODO: Implement inventory clearing
    # Save current inventory before clearing
    # Clear character's inventory list

# ============================================================================
# ITEM USAGE
# ============================================================================

def use_item(character, item_id, item_data):
    """
    Use a consumable item from inventory
    
    Args:
        character: Character dictionary
        item_id: Item to use
        item_data: Item information dictionary from game_data
    
    Item types and effects:
    - consumable: Apply effect and remove from inventory
    - weapon/armor: Cannot be "used", only equipped
    
    Returns: String describing what happened
    Raises: 
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'consumable'
    """
        #  Check item exists
    if item_id not in character["inventory"]:
        raise ItemNotFoundError(f"{item_id} not found in inventory.")

    #  Check item type
    if item_data["type"] != "consumable":
        raise InvalidItemTypeError(f"{item_id} is not a consumable item.")

    #  Parse effect "stat:value"
    stat_name, value = parse_item_effect(item_data["effect"])

    #  Apply effect
    apply_stat_effect(character, stat_name, value)

    # Remove ONE copy of the item
    character["inventory"].remove(item_id)

    item_name = item_data.get("name", item_id)
    return f"You used {item_name} and gained +{value} {stat_name}!"
    # TODO: Implement item usage
    # Check if character has the item
    # Check if item type is 'consumable'
    # Parse effect (format: "stat_name:value" e.g., "health:20")
    # Apply effect to character
    # Remove item from inventory

def equip_weapon(character, item_id, item_data):
    """
    Equip a weapon
    
    Args:
        character: Character dictionary
        item_id: Weapon to equip
        item_data: Item information dictionary
    
    Weapon effect format: "strength:5" (adds 5 to strength)
    
    If character already has weapon equipped:
    - Unequip current weapon (remove bonus)
    - Add old weapon back to inventory
    
    Returns: String describing equipment change
    Raises:
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'weapon'
    """
    # Must have item
    if item_id not in character["inventory"]:
        raise ItemNotFoundError(f"{item_id} not found in inventory.")

    # Must be a weapon
    if item_data["type"] != "weapon":
        raise InvalidItemTypeError(f"{item_id} is not a weapon.")

    # If a weapon is already equipped → unequip it
    if "equipped_weapon" in character and character["equipped_weapon"] is not None:
        
        old_weapon_id = character["equipped_weapon"]

        # Remove old weapon stat bonus
        if "equipped_weapon_effect" in character:
            old_stat, old_value = character["equipped_weapon_effect"]
            apply_stat_effect(character, old_stat, -old_value)

        # Add old weapon back to inventory
        if len(character["inventory"]) >= MAX_INVENTORY_SIZE:
            raise InventoryFullError("No space to unequip old weapon.")

        character["inventory"].append(old_weapon_id)

    # Parse new weapon effect
    stat_name, value = parse_item_effect(item_data["effect"])

    # Apply effect
    apply_stat_effect(character, stat_name, value)

    # Store new weapon
    character["equipped_weapon"] = item_id
    character["equipped_weapon_effect"] = (stat_name, value)

    # Remove from inventory
    character["inventory"].remove(item_id)

    return f"You equipped {item_id} (+{value} {stat_name})."
    # TODO: Implement weapon equipping
    # Check item exists and is type 'weapon'
    # Handle unequipping current weapon if exists
    # Parse effect and apply to character stats
    # Store equipped_weapon in character dictionary
    # Remove item from inventory

def equip_armor(character, item_id, item_data):
    """
    Equip armor
    
    Args:
        character: Character dictionary
        item_id: Armor to equip
        item_data: Item information dictionary
    
    Armor effect format: "max_health:10" (adds 10 to max_health)
    
    If character already has armor equipped:
    - Unequip current armor (remove bonus)
    - Add old armor back to inventory
    
    Returns: String describing equipment change
    Raises:
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'armor'
    """
        #  Must have the item
    if item_id not in character["inventory"]:
        raise ItemNotFoundError(f"{item_id} not found in inventory.")

    #  Must be armor
    if item_data["type"] != "armor":
        raise InvalidItemTypeError(f"{item_id} is not armor.")

    # If armor is already equipped → unequip it
    if "equipped_armor" in character and character["equipped_armor"] is not None:
        old_armor_id = character["equipped_armor"]
        old_armor_data = item_data["all_items"][old_armor_id] if "all_items" in item_data else None

        # Remove old armor stat bonus
        if old_armor_data:
            stat_name, value = parse_item_effect(old_armor_data["effect"])
            apply_stat_effect(character, stat_name, -value)

            # Clamp current health if max_health dropped below health
            if stat_name == "max_health" and character["health"] > character["max_health"]:
                character["health"] = character["max_health"]

        # Add old armor back to inventory
        if len(character["inventory"]) >= MAX_INVENTORY_SIZE:
            raise InventoryFullError("No space to unequip old armor.")

        character["inventory"].append(old_armor_id)

    #  Parse new armor effect
    stat_name, value = parse_item_effect(item_data["effect"])

    #  Apply new armor stats
    apply_stat_effect(character, stat_name, value)

    # Clamp health again if max_health changed
    if stat_name == "max_health" and character["health"] > character["max_health"]:
        character["health"] = character["max_health"]

    #  Save new armor as equipped
    character["equipped_armor"] = item_id

    #  Remove the item from inventory
    character["inventory"].remove(item_id)

    return f"You equipped {item_data['name']} (+{value} {stat_name})."
    # TODO: Implement armor equipping
    # Similar to equip_weapon but for armor

def unequip_weapon(character):
    """
    Remove equipped weapon and return it to inventory
    
    Returns: Item ID that was unequipped, or None if no weapon equipped
    Raises: InventoryFullError if inventory is full
    """
        #  Check if any weapon is equipped
    if "equipped_weapon" not in character or character["equipped_weapon"] is None:
        return None  # nothing to unequip

    weapon_id = character["equipped_weapon"]

    #  Fetch weapon data
    # In game, ALL item_data lives in game_data
    # So equipped items MUST be referenced from there.
    # We'll assume character stores a reference to ALL item data.
    weapon_data = character["all_items"][weapon_id]

    #  Remove stat bonus from character
    stat_name, value = parse_item_effect(weapon_data["effect"])
    apply_stat_effect(character, stat_name, -value)   # subtract the bonus

    #  Inventory must have space to store unequipped weapon
    if len(character["inventory"]) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("No space to return unequipped weapon.")

    #  Add weapon back to inventory
    character["inventory"].append(weapon_id)

    #  Clear equipped_weapon
    character["equipped_weapon"] = None

    #  Return the weapon ID that was unequipped
    return weapon_id

    # TODO: Implement weapon unequipping
    # Check if weapon is equipped
    # Remove stat bonuses
    # Add weapon back to inventory
    # Clear equipped_weapon from character

def unequip_armor(character):
    """
    Remove equipped armor and return it to inventory
    
    Returns: Item ID that was unequipped, or None if no armor equipped
    Raises: InventoryFullError if inventory is full
    """
        #  Check if armor is equipped
    if "equipped_armor" not in character or character["equipped_armor"] is None:
        return None  # nothing to unequip

    armor_id = character["equipped_armor"]

    #  Fetch armor data from all_items
    armor_data = character["all_items"][armor_id]

    #  Remove stat bonus
    stat_name, value = parse_item_effect(armor_data["effect"])

    # Subtract the armor's stat bonus
    apply_stat_effect(character, stat_name, -value)

    #  If max_health dropped below current health → clamp
    if stat_name == "max_health" and character["health"] > character["max_health"]:
        character["health"] = character["max_health"]

    #  Ensure inventory has space
    if len(character["inventory"]) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("No space to return unequipped armor.")

    # Add armor back to inventory
    character["inventory"].append(armor_id)

    # Clear the equipped armor slot
    character["equipped_armor"] = None

    # Return the unequipped armor's ID
    return armor_id

    # TODO: Implement armor unequipping

# ============================================================================
# SHOP SYSTEM
# ============================================================================

def purchase_item(character, item_id, item_data):
    """
    Purchase an item from a shop
    
    Args:
        character: Character dictionary
        item_id: Item to purchase
        item_data: Item information with 'cost' field
    
    Returns: True if purchased successfully
    Raises:
        InsufficientResourcesError if not enough gold
        InventoryFullError if inventory is full
    """
    cost = item_data["cost"]

    #  Check gold
    if character["gold"] < cost:
        raise InsufficientResourcesError("Not enough gold to purchase this item.")

    #  Check inventory space
    if len(character["inventory"]) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory is full.")

    #  Subtract gold
    character["gold"] -= cost

    #  Add item to inventory
    character["inventory"].append(item_id)

    return True

    # TODO: Implement purchasing
    # Check if character has enough gold
    # Check if inventory has space
    # Subtract gold from character
    # Add item to inventory

def sell_item(character, item_id, item_data):
    """
    Sell an item for half its purchase cost
    
    Args:
        character: Character dictionary
        item_id: Item to sell
        item_data: Item information with 'cost' field
    
    Returns: Amount of gold received
    Raises: ItemNotFoundError if item not in inventory
    """
        #  Check if character owns the item
    if item_id not in character["inventory"]:
        raise ItemNotFoundError(f"{item_id} not found in inventory.")

    #  Determine selling price
    sell_price = item_data["cost"] // 2

    #  Remove the item from inventory
    character["inventory"].remove(item_id)

    #  Add gold to the character
    character["gold"] += sell_price

    #  Return the amount earned
    return sell_price

    # TODO: Implement selling
    # Check if character has item
    # Calculate sell price (cost // 2)
    # Remove item from inventory
    # Add gold to character

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_item_effect(effect_string):
    """
    Parse item effect string into stat name and value
    
    Args:
        effect_string: String in format "stat_name:value"
    
    Returns: Tuple of (stat_name, value)
    Example: "health:20" → ("health", 20)
    """
    try:
        stat_name, value_str = effect_string.split(":")
        value = int(value_str)
        return stat_name, value
    except:
        # Effect format is wrong
        raise InvalidItemTypeError(f"Invalid effect format: {effect_string}")
        
    # TODO: Implement effect parsing
    # Split on ":"
    # Convert value to integer

def apply_stat_effect(character, stat_name, value):
    """
    Apply a stat modification to character
    
    Valid stats: health, max_health, strength, magic
    
    Note: health cannot exceed max_health
    """
    #  Modify the stat
    character[stat_name] += value

    #  If modifying max_health, clamp health if needed
    if stat_name == "max_health" and character["health"] > character["max_health"]:
        character["health"] = character["max_health"]

    #  If modifying health, never exceed max_health
    if stat_name == "health" and character["health"] > character["max_health"]:
        character["health"] = character["max_health"]    

    # TODO: Implement stat application
    # Add value to character[stat_name]
    # If stat is health, ensure it doesn't exceed max_health

def display_inventory(character, item_data_dict):
    """
    Display character's inventory in formatted way
    
    Args:
        character: Character dictionary
        item_data_dict: Dictionary of all item data
    
    Shows item names, types, and quantities
    """
    inventory = character["inventory"]

    if not inventory:
        print("Inventory is empty.")
        return

    print("=== INVENTORY ===")

    # Count all items
    item_counts = {}
    for item_id in inventory:
        item_counts[item_id] = item_counts.get(item_id, 0) + 1

    # Display each item with info from item_data_dict
    for item_id, count in item_counts.items():
        item_info = item_data_dict[item_id]
        name = item_info["name"]
        item_type = item_info["type"]

        print(f"{name} ({item_type}) x{count}")
    # TODO: Implement inventory display
    # Count items (some may appear multiple times)
    # Display with item names from item_data_dict

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== INVENTORY SYSTEM TEST ===")
    
    # Test adding items
    test_char = {'inventory': [], 'gold': 100, 'health': 80, 'max_health': 80}
    # 
    try:
        add_item_to_inventory(test_char, "health_potion")
        print(f"Inventory: {test_char['inventory']}")
    except InventoryFullError:
        print("Inventory is full!")
    
    # Test using items
    test_item = {
        'item_id': 'health_potion',
        'type': 'consumable',
        'effect': 'health:20'
    }
    # 
    try:
        result = use_item(test_char, "health_potion", test_item)
        print(result)
    except ItemNotFoundError:
        print("Item not found")

