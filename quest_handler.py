"""
COMP 163 - Project 3: Quest Chronicles
Quest Handler Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This module handles quest management, dependencies, and completion.
"""

from custom_exceptions import (
    QuestNotFoundError,
    QuestRequirementsNotMetError,
    QuestAlreadyCompletedError,
    QuestNotActiveError,
    InsufficientLevelError
)

# ============================================================================
# QUEST MANAGEMENT
# ============================================================================

def accept_quest(character, quest_id, quest_data_dict):
    """
    Accept a new quest
    
    Args:
        character: Character dictionary
        quest_id: Quest to accept
        quest_data_dict: Dictionary of all quest data
    
    Requirements to accept quest:
    - Character level >= quest required_level
    - Prerequisite quest completed (if any)
    - Quest not already completed
    - Quest not already active
    
    Returns: True if quest accepted
    Raises:
        QuestNotFoundError if quest_id not in quest_data_dict
        InsufficientLevelError if character level too low
        QuestRequirementsNotMetError if prerequisite not completed
        QuestAlreadyCompletedError if quest already done
    """
    #quest must exist
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest '{quest_id}' does not exist.")
    
    quest = quest_data_dict[quest_id]

    #level requirement
    if character['level'] < quest['required_level']:
        raise InsufficientLevelError(f"Level {quest['required_level']} required to accept this quest.")
    
    #prerequisite check
    prereq = quest['prerequisite']
    if prereq != "NONE" and prereq not in character['completed_quests']:
        raise QuestRequirementsNotMetError(f"Prerequisite quest '{prereq}' not completed.")
    
    #already completed check
    if quest_id in character['completed_quests']:
        raise QuestAlreadyCompletedError(f"Quest '{quest_id}' has already been completed.")
    
    #already active check
    if quest_id in character['active_quests']:
        raise QuestRequirementsNotMetError(f"Quest '{quest_id}' is already active.")
    
    #add to active quests
    character['active_quests'].append(quest_id)

    return True

    # TODO: Implement quest acceptance
    # Check quest exists
    # Check level requirement
    # Check prerequisite (if not "NONE")
    # Check not already completed
    # Check not already active
    # Add to character['active_quests']

def complete_quest(character, quest_id, quest_data_dict):
    """
    Complete an active quest and grant rewards
    
    Args:
        character: Character dictionary
        quest_id: Quest to complete
        quest_data_dict: Dictionary of all quest data
    
    Rewards:
    - Experience points (reward_xp)
    - Gold (reward_gold)
    
    Returns: Dictionary with reward information
    Raises:
        QuestNotFoundError if quest_id not in quest_data_dict
        QuestNotActiveError if quest not in active_quests
    """

    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest '{quest_id}' does not exist.")
    
    #quest must be active
    if quest_id not in character['active_quests']:
        raise QuestNotActiveError(f"Quest '{quest_id}' is not currently active.")
    
    quest = quest_data_dict[quest_id]

    #remove from active quests
    character['active_quests'].remove(quest_id)
    #add to completed quests
    character['completed_quests'].append(quest_id)

    #grant rewards
    xp_reward = quest["reward_xp"]
    gold_reward = quest["reward_gold"]

    character['experience'] += xp_reward
    character['gold'] += gold_reward

    return {
        "reward_xp": xp_reward,
        "reward_gold": gold_reward,
        "quest_title": quest["title"]
    }


    # TODO: Implement quest completion
    # Check quest exists
    # Check quest is active
    # Remove from active_quests
    # Add to completed_quests
    # Grant rewards (use character_manager.gain_experience and add_gold)
    # Return reward summary

def abandon_quest(character, quest_id):
    """
    Remove a quest from active quests without completing it
    
    Returns: True if abandoned
    Raises: QuestNotActiveError if quest not active
    """
    #quest must be active
    if quest_id not in character['active_quests']:
        raise QuestNotActiveError(f"Quest '{quest_id}' is not currently active.")
    
    #remove from active quests
    character['active_quests'].remove(quest_id)
    return True

    # TODO: Implement quest abandonment

def get_active_quests(character, quest_data_dict):
    """
    Get full data for all active quests
    
    Returns: List of quest dictionaries for active quests
    """
    active_list = []

    for quest_id in character['active_quests']:
        if quest_id in quest_data_dict: #safety check
            active_list.append(quest_data_dict[quest_id])

    return active_list

    # TODO: Implement active quest retrieval
    # Look up each quest_id in character['active_quests']
    # Return list of full quest data dictionaries

def get_completed_quests(character, quest_data_dict):
    """
    Get full data for all completed quests
    
    Returns: List of quest dictionaries for completed quests
    """
    completed_list = []

    for quest_id in character["completed_quests"]:
        if quest_id in quest_data_dict:  # Safety check
            completed_list.append(quest_data_dict[quest_id]) #Adds full dictionary to list

    return completed_list

    # TODO: Implement completed quest retrieval

def get_available_quests(character, quest_data_dict):
    """
    Get quests that character can currently accept
    
    Available = meets level req + prerequisite done + not completed + not active
    
    Returns: List of quest dictionaries
    """

    available = []

    for quest_id, quest in quest_data_dict.items():
        # Check level requirement
        if character['level'] < quest['required_level']:
            continue
        
        # Check prerequisite
        prereq = quest['prerequisite']
        if prereq != "NONE" and prereq not in character['completed_quests']:
            continue
        
        # Check not already completed
        if quest_id in character['completed_quests']:
            continue
        
        # Check not already active
        if quest_id in character['active_quests']:
            continue
        
        # If all checks passed, add to available quests
        available.append(quest)

    return available
    # TODO: Implement available quest search
    # Filter all quests by requirements

# ============================================================================
# QUEST TRACKING
# ============================================================================

def is_quest_completed(character, quest_id):
    """
    Check if a specific quest has been completed
    
    Returns: True if completed, False otherwise
    """
    #checks if quest_id is in completed quests
    return quest_id in character['completed_quests']
    # TODO: Implement completion check

def is_quest_active(character, quest_id):
    """
    Check if a specific quest is currently active
    
    Returns: True if active, False otherwise
    """
    #checks if quest_id is in active quests
    return quest_id in character['active_quests']
    # TODO: Implement active check

def can_accept_quest(character, quest_id, quest_data_dict):
    """
    Check if character meets all requirements to accept quest
    
    Returns: True if can accept, False otherwise
    Does NOT raise exceptions - just returns boolean
    """
    #quest must exist in database
    if quest_id not in quest_data_dict:
        return False
    quest = quest_data_dict[quest_id]

    #level requirement
    if character['level'] < quest['required_level']:
        return False
    
    #prerequisite check
    prereq = quest['prerequisite']
    if prereq != "NONE" and prereq not in character['completed_quests']:
        return False
    
    #already completed check
    if quest_id in character['completed_quests']:
        return False
    
    #already active check
    if quest_id in character['active_quests']:
        return False
    
    return True
    # TODO: Implement requirement checking
    # Check all requirements without raising exceptions

def get_quest_prerequisite_chain(quest_id, quest_data_dict):
    """
    Get the full chain of prerequisites for a quest
    
    Returns: List of quest IDs in order [earliest_prereq, ..., quest_id]
    Example: If Quest C requires Quest B, which requires Quest A:
            Returns ["quest_a", "quest_b", "quest_c"]
    
    Raises: QuestNotFoundError if quest doesn't exist
    """
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest '{quest_id}' does not exist.")
    
    chain = []
    current_quest_id = quest_id

    while True:
        if current_quest_id not in quest_data_dict:
            raise QuestNotFoundError(f"Quest '{current_quest_id}' does not exist.")
        #adds quest to chain
        chain.append(current_quest_id)
        #looks at prerequisite for quest
        prerequisite = quest_data_dict[current_quest_id]['prerequisite']
        if prerequisite == "NONE":
            break

        current_quest_id = prerequisite

    chain.reverse()  # Reverse to get earliest prerequisite first
    return chain

    # TODO: Implement prerequisite chain tracing
    # Follow prerequisite links backwards
    # Build list in reverse order

# ============================================================================
# QUEST STATISTICS
# ============================================================================

def get_quest_completion_percentage(character, quest_data_dict):
    """
    Calculate what percentage of all quests have been completed
    
    Returns: Float between 0 and 100
    """
    #total quests in the game 
    total_quests = len(quest_data_dict)

    #If there are no quest defined, return 0.0 to avoid division by zero
    if total_quests == 0:
        return 0.0
    
    #number of completed quests by character
    completed_quests = len(character['completed_quests'])

    #calculate percentage
    percentage = (completed_quests / total_quests) * 100
    return percentage

    # TODO: Implement percentage calculation
    # total_quests = len(quest_data_dict)
    # completed_quests = len(character['completed_quests'])
    # percentage = (completed / total) * 100

def get_total_quest_rewards_earned(character, quest_data_dict):
    """
    Calculate total XP and gold earned from completed quests
    
    Returns: Dictionary with 'total_xp' and 'total_gold'
    """
    total_xp = 0
    total_gold = 0

    # Loop through each completed quest ID
    for quest_id in character["completed_quests"]:

        # Make sure this quest exists in the quest database
        if quest_id in quest_data_dict:

            quest = quest_data_dict[quest_id]

            # Add the XP reward
            total_xp += quest["reward_xp"]

            # Add the gold reward
            total_gold += quest["reward_gold"]

    # Return results in a dictionary
    return {
        "total_xp": total_xp,
        "total_gold": total_gold
    }
    # TODO: Implement reward calculation
    # Sum up reward_xp and reward_gold for all completed quests

def get_quests_by_level(quest_data_dict, min_level, max_level):
    """
    Get all quests within a level range
    
    Returns: List of quest dictionaries
    """
    results = []  # list of quests we will return

    # Loop through every quest in the dictionary
    for quest_id, quest in quest_data_dict.items():

        # Extract the required level for this quest
        level = quest["required_level"]

        # Check if the level fits within the range (inclusive)
        if min_level <= level <= max_level:
            results.append(quest)

    return results
    # TODO: Implement level filtering

# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================

def display_quest_info(quest_data):
    """
    Display formatted quest information
    
    Shows: Title, Description, Rewards, Requirements
    """
    print(f"\n=== {quest_data['title']} ===")
    print(f"Description: {quest_data['description']}")
    print(f"Required Level: {quest_data['required_level']}")
    print(f"Prerequisite: {quest_data['prerequisite']}")
    print(f"Reward XP: {quest_data['reward_xp']}")
    print(f"Reward Gold: {quest_data['reward_gold']}")

def display_quest_list(quest_list):
    """
    Display a list of quests in summary format
    
    Shows: Title, Required Level, Rewards
    """
    if not quest_list:
        print("No quests to display.")
        return
    print("\n=== Available Quest ===")
    for quest in quest_list:
        print(f"- {quest['title']} (Level {quest['required_level']})")
        print(f"  Rewards: {quest['reward_xp']} XP, {quest['reward_gold']} Gold")
        print() #blank line in between quest


    # TODO: Implement quest list display

def display_character_quest_progress(character, quest_data_dict):
    """
    Display character's quest statistics and progress
    
    Shows:
    - Active quests count
    - Completed quests count
    - Completion percentage
    - Total rewards earned
    """
    # Number of quests the character has taken but not finished
    active_count = len(character['active_quests'])

    # Number of quests fully completed
    completed_count = len(character['completed_quests'])

    # What % of all quests in the game are completed
    completion_percentage = get_quest_completion_percentage(character, quest_data_dict)

    # Amount of XP + gold earned from completed quests
    total_rewards = get_total_quest_rewards_earned(character, quest_data_dict)

    print("\n=== QUEST PROGRESS ===")
    print(f"Active Quests: {active_count}")
    print(f"Completed Quests: {completed_count}")
    print(f"Completion: {completion_percentage:.2f}%")
    print(f"Total XP Earned: {total_rewards['total_xp']}")
    print(f"Total Gold Earned: {total_rewards['total_gold']}")
    # TODO: Implement progress display

# ============================================================================
# VALIDATION
# ============================================================================

def validate_quest_prerequisites(quest_data_dict):
    """
    Validate that all quest prerequisites exist
    
    Checks that every prerequisite (that's not "NONE") refers to a real quest
    
    Returns: True if all valid
    Raises: QuestNotFoundError if invalid prerequisite found
    """
    # Loop through EVERY quest in the dictionary
    for quest_id, quest in quest_data_dict.items():

        prereq = quest['prerequisite']  # ex: "first_quest"

        # If quest has no prerequisite, skip it
        if prereq == "NONE":
            continue

        # If prerequisite name is not found in the list of quests
        if prereq not in quest_data_dict:
            raise QuestNotFoundError(
                f"Prerequisite '{prereq}' for quest '{quest_id}' does not exist."
            )

    # If loop finishes with no errors, everything is valid
    return True
    # TODO: Implement prerequisite validation
    # Check each quest's prerequisite
    # Ensure prerequisite exists in quest_data_dict


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== QUEST HANDLER TEST ===")
    
    # Test data
    test_char = {
        'level': 1,
        'active_quests': [],
        'completed_quests': [],
        'experience': 0,
        'gold': 100
    }
    
    test_quests = {
        'first_quest': {
            'quest_id': 'first_quest',
            'title': 'First Steps',
            'description': 'Complete your first quest',
            'reward_xp': 50,
            'reward_gold': 25,
            'required_level': 1,
            'prerequisite': 'NONE'
        }
    }
    
    try:
        accept_quest(test_char, 'first_quest', test_quests)
        print("Quest accepted!")
    except QuestRequirementsNotMetError as e:
        print(f"Cannot accept: {e}")

