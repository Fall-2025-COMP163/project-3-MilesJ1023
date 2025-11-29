[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/wnCpjX4n)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=21830313&assignment_repo_type=AssignmentRepo)
README – Quest Chronicles (COMP 163 Project 3) Miles Johnson

Quest Chronicles is a modular, text-based RPG designed to demonstrate Python skills related to modules, exceptions, file handling, and structured program design.
The project is split across multiple files so each system of the game is clearly separated and easier to test.

Project Structure
quest_chronicles/
│
├── main.py                 # Main menu and overall game flow
├── character_manager.py    # Character creation, saving, loading, leveling, stats
├── inventory_system.py     # Inventory logic, equipment, item usage, shop
├── quest_handler.py        # Quest acceptance, completion, prerequisite logic
├── combat_system.py        # Turn-based combat, abilities, enemies
├── game_data.py            # Loading and validating quests/items from files
├── custom_exceptions.py    # Custom-defined exceptions used throughout
│
└── data/
    ├── quests.txt
    ├── items.txt
    └── save_games/


Each module handles one focused part of the game.
This makes the code cleaner and prevents one file from becoming unmanageably large.

Gameplay Summary
Character Creation

Players choose a name and one of the required classes (Warrior, Mage, Rogue, Cleric).
Base stats differ by class, and characters begin at level 1.

Exploration and Combat

The explore option generates a random enemy based on the player’s level.
Combat is turn-based, and each class has its own special ability.

Quests

Players can view available quests, accept them if they meet the requirements, and complete them for rewards.
The system also handles prerequisite chaining (a quest may require another quest to be finished first).

Inventory System

The player can pick up items, equip weapons and armor, use consumables, and buy or sell items in shops.
All item effects follow a consistent stat:value format.

Saving and Loading

Character data is saved as a text file inside data/save_games.
The game can be fully exited and resumed later.

Module Overview
1. game_data.py

Loads item and quest definitions from text files and validates formatting.
Also creates default files if they don’t exist.

2. character_manager.py

Handles character creation, stat updates, saving/loading, leveling, and death/revival.

3. inventory_system.py

Manages inventory capacity, item usage, equipment, stat effects, and the in-game shop.

4. quest_handler.py

Handles quest acceptance rules, quest completion, prerequisite checking, and progress statistics.

5. combat_system.py

Handles enemy creation, turn sequence, damage calculation, escaping, and class abilities.

6. main.py

Provides all menus, the main game loop, and connects every system together.

Exception Strategy

The project defines a set of custom exceptions to keep error handling clear and consistent.
Examples include:

MissingDataFileError

InvalidDataFormatError

CharacterNotFoundError

InventoryFullError

ItemNotFoundError

QuestNotFoundError

InsufficientLevelError

CharacterDeadError

AbilityOnCooldownError

Each module raises specific exceptions when something goes wrong, which makes debugging easier and satisfies project requirements.

Running the Game

From the project directory, run:

python main.py


The game will load necessary data, show the main menu, and allow the player to start a new game or load an existing one.

Testing

The project includes automated integration tests that verify:

Character creation and saving

Leveling

Inventory and equipment

Combat

Quest acceptance and prerequisites

Data validation

Game workflow

All modules were written so that these tests pass successfully.

AI Usage Statement

I used AI (ChatGPT) as a learning assistant during parts of this project.
It helped me:

Understand how to structure the modules cleanly

Clarify certain programming concepts like parsing, exception flow, and modular design

Work through errors related to equipment handling and save-file parsing

Get explanations and guidance when debugging my own code

Understand how to read and satisfy the provided test cases

All final logic, decisions, and code implementation were written by me.
AI was used for explanation and support, not for generating a full program.
