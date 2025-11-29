"""
COMP 163 - Project 3: Quest Chronicles
Main Game Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This is the main game file that ties all modules together.
Demonstrates module integration and complete game flow.
"""

# Import all our custom modules
import character_manager
import inventory_system
import quest_handler
import combat_system
import game_data
from custom_exceptions import *

# ============================================================================
# GAME STATE
# ============================================================================

# Global variables for game data
current_character = None
all_quests = {}
all_items = {}
game_running = False

# ============================================================================
# MAIN MENU
# ============================================================================

def main_menu():
    """
    Display main menu and get player choice
    
    Options:
    1. New Game
    2. Load Game
    3. Exit
    
    Returns: Integer choice (1-3)
    """
    print("\n=== MAIN MENU ===")
    print("1. New Game")
    print("2. Load Game")
    print("3. Exit")

    choice = input("Enter your choice (1-3): ").strip()
    if choice in ['1', '2', '3']:
        return int(choice)
    
    print("Invalid choice. Please select 1-3.")
    return main_menu()

    # TODO: Implement main menu display
    # Show options
    # Get user input
    # Validate input (1-3)
    # Return choice

def new_game():
    """
    Start a new game
    
    Prompts for:
    - Character name
    - Character class
    
    Creates character and starts game loop
    """
    global current_character

    print("\n=== NEW GAME ===")

    name = input("Enter your character's name: ").strip()
    print("Choose your character class:")
    print("1. Warrior")
    print("2. Mage")
    print("3. Rogue")
    print("4. Cleric")

    class_choice = input("Enter your choice (1-4): ").strip()

    class_dict = {'1': 'Warrior', '2': 'Mage', '3': 'Rogue', '4': 'Cleric'}
    
    if class_choice not in class_dict:
        print("Invalid choice. Please select 1-4.")
        return new_game()
    char_class = class_dict[class_choice]

    try:
        current_character = character_manager.create_character(name, char_class)
        print(f"Character '{name}' the {char_class} created successfully!")
    except InvalidCharacterClassError:
        print("Error creating character. Please try again.")
        return
    
    character_manager.save_character(current_character)
    print("Character saved. Starting game...")
    game_loop()
    
    # TODO: Implement new game creation
    # Get character name from user
    # Get character class from user
    # Try to create character with character_manager.create_character()
    # Handle InvalidCharacterClassError
    # Save character
    # Start game loop

def load_game():
    """
    Load an existing saved game
    
    Shows list of saved characters
    Prompts user to select one
    """
    global current_character
    print("\n=== LOAD GAME ===")

    # Get all saved character names
    saved = character_manager.list_saved_characters()

    # If no saves exist
    if not saved:
        print("No saved characters found.")
        return

    # Display list
    print("\nSaved Characters:")
    for i, name in enumerate(saved, start=1):
        print(f"{i}. {name}")

    # Ask player to choose one
    choice = input("\nEnter the number of the character to load: ").strip()

    # Validate input: must be a number
    if not choice.isdigit():
        print("Invalid selection.")
        return

    choice = int(choice)

    # Check if number corresponds to a save
    if choice < 1 or choice > len(saved):
        print("Invalid selection.")
        return

    selected_name = saved[choice - 1]

    # Try loading the character
    try:
        current_character = character_manager.load_character(selected_name)
        print(f"\nLoaded character: {current_character['name']} the {current_character['class']}!")
    except CharacterNotFoundError:
        print("Save file not found.")
        return
    except SaveFileCorruptedError:
        print("Save file is corrupted.")
        return
    except InvalidSaveDataError:
        print("Save data is invalid.")
        return

    # Enter game loop
    game_loop()

    # TODO: Implement game loading
    # Get list of saved characters
    # Display them to user
    # Get user choice
    # Try to load character with character_manager.load_character()
    # Handle CharacterNotFoundError and SaveFileCorruptedError
    # Start game loop

# ============================================================================
# GAME LOOP
# ============================================================================

def game_loop():
    """
    Main game loop - shows game menu and processes actions
    """
    global game_running, current_character
    
    game_running = True

    while game_running:
        choice = game_menu()
        
        if choice == 1:
            view_character_stats()
        elif choice == 2:
            view_inventory()
        elif choice == 3:
            quest_menu()
        elif choice == 4:
            explore()
        elif choice == 5:
            shop()
        elif choice == 6:
            save_game()
            print("Game saved. Exiting to main menu.")
            game_running = False
        else:
            print("Invalid choice. Please select a valid option.")
    
    # TODO: Implement game loop
    # While game_running:
    #   Display game menu
    #   Get player choice
    #   Execute chosen action
    #   Save game after each action

def game_menu():
    """
    Display game menu and get player choice
    
    Options:
    1. View Character Stats
    2. View Inventory
    3. Quest Menu
    4. Explore (Find Battles)
    5. Shop
    6. Save and Quit
    
    Returns: Integer choice (1-6)
    """
    print("\n=== GAME MENU ===")
    print("1. View Character Stats")
    print("2. View Inventory")
    print("3. Quest Menu")
    print("4. Explore (Find Battles)")
    print("5. Shop")
    print("6. Save and Quit")

    choice = input("Choose an option (1-6): ").strip()

    # Validate input
    if choice in ["1", "2", "3", "4", "5", "6"]:
        return int(choice)

    print("Invalid choice. Please enter a number from 1 to 6.")
    return game_menu()  # Ask again
    # TODO: Implement game menu

# ============================================================================
# GAME ACTIONS
# ============================================================================

def view_character_stats():
    """Display character information"""
    global current_character

    char = current_character  # shorthand

    print("\n=== CHARACTER STATS ===")
    print(f"Name: {char['name']}")
    print(f"Class: {char['class']}")
    print(f"Level: {char['level']}")
    print(f"Experience: {char['experience']}")
    print(f"Gold: {char['gold']}")
    print()
    print(f"Health: {char['health']} / {char['max_health']}")
    print(f"Strength: {char['strength']}")
    print(f"Magic: {char['magic']}")
    print()
    print(f"Active Quests: {len(char['active_quests'])}")
    print(f"Completed Quests: {len(char['completed_quests'])}")
    print()

    input("Press ENTER to continue...")

    # TODO: Implement stats display
    # Show: name, class, level, health, stats, gold, etc.
    # Use character_manager functions
    # Show quest progress using quest_handler

def view_inventory():
    """Display and manage inventory"""
    global current_character, all_items

    while True:
        print("\n=== INVENTORY ===")
        inventory_system.display_inventory(current_character, all_items)

        print("\nOptions:")
        print("1. Use Item (consumable)")
        print("2. Equip Weapon")
        print("3. Equip Armor")
        print("4. Drop Item")
        print("5. Back")

        choice = input("Choose an option (1-5): ").strip()

        # BACK
        if choice == "5":
            return

        item_id = input("Enter the ITEM ID: ").strip()

        # Validate item exists in global item database
        if item_id not in all_items:
            print("Item does not exist in item database.")
            continue
        
        item_data = all_items[item_id]

        # 1. USE ITEM
        if choice == "1":
            try:
                result = inventory_system.use_item(current_character, item_id, item_data)
                print(result)
            except ItemNotFoundError:
                print("You don't have that item.")
            except InvalidItemTypeError:
                print("That item cannot be used.")
        
        # 2. EQUIP WEAPON
        elif choice == "2":
            try:
                result = inventory_system.equip_weapon(current_character, item_id, item_data)
                print(result)
            except ItemNotFoundError:
                print("You don't have that weapon.")
            except InvalidItemTypeError:
                print("That is not a weapon.")
        
        # 3. EQUIP ARMOR
        elif choice == "3":
            try:
                result = inventory_system.equip_armor(current_character, item_id, item_data)
                print(result)
            except ItemNotFoundError:
                print("You don't have that armor.")
            except InvalidItemTypeError:
                print("That is not armor.")

        # 4. DROP ITEM
        elif choice == "4":
            try:
                inventory_system.remove_item_from_inventory(current_character, item_id)
                print(f"Dropped {item_id}.")
            except ItemNotFoundError:
                print("You don't have that item.")

        else:
            print("Invalid choice.")
    # TODO: Implement inventory menu
    # Show current inventory
    # Options: Use item, Equip weapon/armor, Drop item
    # Handle exceptions from inventory_system

def quest_menu():
    """Quest management menu"""
    global current_character, all_quests
    
    while True:
        print("\n=== QUEST MENU ===")
        print("1. View Active Quests")
        print("2. View Available Quests")
        print("3. View Completed Quests")
        print("4. Accept a Quest")
        print("5. Abandon a Quest")
        print("6. Complete Quest (testing)")
        print("7. Back")

        choice = input("Choose an option (1-7): ").strip()

        # 7. BACK
        if choice == "7":
            return

        # 1. ACTIVE QUESTS
        if choice == "1":
            active = quest_handler.get_active_quests(current_character, all_quests)
            quest_handler.display_quest_list(active)
            input("\nPress ENTER to continue...")
            continue

        # 2. AVAILABLE QUESTS
        if choice == "2":
            available = quest_handler.get_available_quests(current_character, all_quests)
            quest_handler.display_quest_list(available)
            input("\nPress ENTER to continue...")
            continue


        # 3. COMPLETED QUESTS
        if choice == "3":
            completed = quest_handler.get_completed_quests(current_character, all_quests)
            quest_handler.display_quest_list(completed)
            input("\nPress ENTER to continue...")
            continue

        # 4. ACCEPT QUEST
        if choice == "4":
            quest_id = input("Enter Quest ID to accept: ").strip()

            try:
                quest_handler.accept_quest(current_character, quest_id, all_quests)
                print("Quest accepted!")
            except QuestNotFoundError:
                print("That quest does not exist.")
            except InsufficientLevelError:
                print("Your level is too low for this quest.")
            except QuestRequirementsNotMetError:
                print("You have not met the prerequisite for this quest.")
            except QuestAlreadyCompletedError:
                print("You already completed this quest.")

            input("\nPress ENTER to continue...")
            continue

        # 5. ABANDON QUEST
        if choice == "5":
            quest_id = input("Enter Quest ID to abandon: ").strip()

            try:
                quest_handler.abandon_quest(current_character, quest_id)
                print("Quest abandoned.")
            except QuestNotActiveError:
                print("This quest is not currently active.")

            input("\nPress ENTER to continue...")
            continue

        # 6. COMPLETE QUEST (TESTING)
        if choice == "6":
            quest_id = input("Enter Quest ID to complete: ").strip()

            try:
                rewards = quest_handler.complete_quest(current_character, quest_id, all_quests)
                print(f"Quest completed! You earned {rewards['xp']} XP and {rewards['gold']} gold.")
            except QuestNotFoundError:
                print("Quest does not exist.")
            except QuestNotActiveError:
                print("Quest is not active.")

            input("\nPress ENTER to continue...")
            continue


        # INVALID OPTION
        print("Invalid choice. Please choose between 1 and 7.")
    # TODO: Implement quest menu
    # Show:
    #   1. View Active Quests
    #   2. View Available Quests
    #   3. View Completed Quests
    #   4. Accept Quest
    #   5. Abandon Quest
    #   6. Complete Quest (for testing)
    #   7. Back
    # Handle exceptions from quest_handler

def explore():
    """Find and fight random enemies"""
    global current_character
    print("\n=== EXPLORING... ===")

    # Choose enemy based on player level
    enemy = combat_system.get_random_enemy_for_level(current_character["level"])
    print(f"\nA wild {enemy['name']} appears!")

    # Start battle
    battle = combat_system.SimpleBattle(current_character, enemy)

    try:
        result = battle.start_battle()
    except CharacterDeadError:
        handle_character_death()
        return  # stop here after death handling

    # Display result summary
    print("\n=== BATTLE RESULTS ===")

    if result["winner"] == "player":
        print("You won the battle!")
        print(f"XP Gained: {result['xp_gained']}")
        print(f"Gold Gained: {result['gold_gained']}")

    elif result["winner"] == "enemy":
        print("You were defeated!")
        handle_character_death()
        return
    
    else:
        print("You escaped safely!")

    # Pause before returning to game loop
    input("\nPress ENTER to continue...")
    # TODO: Implement exploration
    # Generate random enemy based on character level
    # Start combat with combat_system.SimpleBattle
    # Handle combat results (XP, gold, death)
    # Handle exceptions

def shop():
    """Shop menu for buying/selling items"""
    global current_character, all_items
    while True:
        print("\n=== SHOP ===")
        print(f"Your Gold: {current_character['gold']}")
        print("\nItems for Sale:")

        # Display items with cost and type
        for item_id, item in all_items.items():
            print(f"- {item_id}: {item['name']} ({item['type']}), Cost: {item['cost']}")

        print("\nOptions:")
        print("1. Buy Item")
        print("2. Sell Item")
        print("3. Back")

        choice = input("Choose an option (1-3): ").strip()

        # BACK
        if choice == "3":
            return

        # BUY ITEM
        if choice == "1":
            item_id = input("Enter ITEM ID to buy: ").strip()

            if item_id not in all_items:
                print("Item does not exist in shop.")
                continue

            item_data = all_items[item_id]

            try:
                inventory_system.purchase_item(current_character, item_id, item_data)
                print(f"Purchased {item_data['name']}!")
            except InsufficientResourcesError:
                print("You do not have enough gold.")
            except InventoryFullError:
                print("Your inventory is full.")

            input("\nPress ENTER to continue...")
            continue

        # SELL ITEM
        if choice == "2":
            item_id = input("Enter ITEM ID to sell: ").strip()

            if item_id not in all_items:
                print("Item does not exist.")
                continue

            item_data = all_items[item_id]

            try:
                gold_gained = inventory_system.sell_item(current_character, item_id, item_data)
                print(f"Sold {item_data['name']} for {gold_gained} gold!")
            except ItemNotFoundError:
                print("You do not have that item in your inventory.")

            input("\nPress ENTER to continue...")
            continue

        # INVALID INPUT
        print("Invalid choice.")

    # TODO: Implement shop
    # Show available items for purchase
    # Show current gold
    # Options: Buy item, Sell item, Back
    # Handle exceptions from inventory_system

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def save_game():
    """Save current game state"""
    global current_character
    
    if current_character is None:
        print("No character to save.")
        return

    try:
        character_manager.save_character(current_character)
        print("\nGame saved successfully!")
    except PermissionError:
        print("Error: You don't have permission to save the file.")
    except IOError:
        print("Error: Could not write save file. Check folder permissions.")
    # TODO: Implement save
    # Use character_manager.save_character()
    # Handle any file I/O exceptions

def load_game_data():
    """Load all quest and item data from files"""
    global all_quests, all_items
    try:
        # Try loading quests and items
        all_quests = game_data.load_quests()
        all_items = game_data.load_items()

    except MissingDataFileError:
        # If files don't exist, create defaults and reload
        print("Data files missing. Creating default files...")
        game_data.create_default_data_files()

        all_quests = game_data.load_quests()
        all_items = game_data.load_items()

    except InvalidDataFormatError as e:
        print(f"Error: Invalid game data format - {e}")
        raise  # Stop program because bad data cannot be used

    # TODO: Implement data loading
    # Try to load quests with game_data.load_quests()
    # Try to load items with game_data.load_items()
    # Handle MissingDataFileError, InvalidDataFormatError
    # If files missing, create defaults with game_data.create_default_data_files()

def handle_character_death():
    """Handle character death"""
    global current_character, game_running

    print("\n Your character has fallen in battle!")
    print("1. Revive for 50 gold")
    print("2. Quit to main menu")

    while True:
        choice = input("Choose an option (1-2): ").strip()

        # ---- Option 1: Revive ----
        if choice == "1":
            if current_character["gold"] < 50:
                print("You do not have enough gold to revive! Returning to main menu.")
                game_running = False
                return

            # Pay gold
            current_character["gold"] -= 50

            # Revive using character_manager
            character_manager.revive_character(current_character)

            print("✨ You have been revived at 50% HP!")
            return  # go back to game loop

        # ---- Option 2: Quit ----
        elif choice == "2":
            print("Returning to main menu...")
            game_running = False
            return

        else:
            print("Invalid choice. Please enter 1 or 2.")
    # TODO: Implement death handling
    # Display death message
    # Offer: Revive (costs gold) or Quit
    # If revive: use character_manager.revive_character()
    # If quit: set game_running = False

def display_welcome():
    """Display welcome message"""
    print("=" * 50)
    print("     QUEST CHRONICLES - A MODULAR RPG ADVENTURE")
    print("=" * 50)
    print("\nWelcome to Quest Chronicles!")
    print("Build your character, complete quests, and become a legend!")
    print()

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main game execution function"""
    
    # Display welcome message
    display_welcome()
    
    # Load game data
    try:
        load_game_data()
        print("Game data loaded successfully!")
    except MissingDataFileError:
        print("Creating default game data...")
        game_data.create_default_data_files()
        load_game_data()
    except InvalidDataFormatError as e:
        print(f"Error loading game data: {e}")
        print("Please check data files for errors.")
        return
    
    # Main menu loop
    while True:
        choice = main_menu()
        
        if choice == 1:
            new_game()
        elif choice == 2:
            load_game()
        elif choice == 3:
            print("\nThanks for playing Quest Chronicles!")
            break
        else:
            print("Invalid choice. Please select 1-3.")

if __name__ == "__main__":
    main()

