from flask import Flask, render_template, request, jsonify
import random
import time

app = Flask(__name__)

# Game state to track the simulation progress
game_state = {
    "current_region_index": 0,
    "current_round": 1,
    "current_matchup_index": 0,
    "regions_completed": 0,
    "champions": [],
    "region_winners": [],
    "matchups": [],
    "current_matchup": None,
    "messages": [],
    "waiting_for_input": False,
    "game_over": False,
    "final_four_stage": 0,  # 0: not started, 1: semifinal 1, 2: semifinal 2, 3: championship
}

# ======================== ORIGINAL SIMULATOR FUNCTIONS ========================

def get_first_round_upset_chance(seed1, seed2):
    """Returns the correct upset chance for first round matchups"""
    # Higher seed is the one with the lower number
    higher_seed = min(seed1, seed2)
    lower_seed = max(seed1, seed2)
    
    # Explicit mapping for first round matchups
    if higher_seed == 1 and lower_seed == 16:
        return 2.5
    elif higher_seed == 8 and lower_seed == 9:
        return 50.0
    elif higher_seed == 5 and lower_seed == 12:
        return 25.0
    elif higher_seed == 4 and lower_seed == 13:
        return 20.0
    elif higher_seed == 6 and lower_seed == 11:
        return 33.0
    elif higher_seed == 3 and lower_seed == 14:
        return 20.0
    elif higher_seed == 7 and lower_seed == 10:
        return 33.0
    elif higher_seed == 2 and lower_seed == 15:
        return 8.33
    else:
        return 0.0  # Default

def get_second_round_upset_chance(seed1, seed2):
    """Returns the correct upset chance for second round matchups"""
    # Higher seed is the one with the lower number
    higher_seed = min(seed1, seed2)
    lower_seed = max(seed1, seed2)
    
    # 1 seed matchups (updated)
    if higher_seed == 1 and lower_seed in [8, 9]:
        return 25.0
    elif higher_seed in [8, 9] and lower_seed == 16:
        return 25.0
    
    # 4/5 region matchups (updated)
    elif higher_seed == 4 and lower_seed == 5:
        return 50.0
    elif higher_seed == 4 and lower_seed == 12:
        return 25.0
    elif higher_seed == 5 and lower_seed == 13:
        return 25.0
    elif higher_seed == 12 and lower_seed == 13:
        return 50.0
    
    # 3/6 region matchups (updated)
    elif higher_seed == 3 and lower_seed == 6:
        return 33.0
    elif higher_seed == 3 and lower_seed == 11:
        return 25.0
    elif higher_seed == 6 and lower_seed == 14:
        return 33.0
    elif higher_seed == 11 and lower_seed == 14:
        return 50.0
    
    # 2/7 region matchups (updated)
    elif higher_seed == 2 and lower_seed == 7:
        return 33.0
    elif higher_seed == 2 and lower_seed == 10:
        return 25.0
    elif higher_seed == 7 and lower_seed == 15:
        return 25.0
    elif higher_seed == 10 and lower_seed == 15:
        return 33.0
    
    else:
        return 0.0  # Default

def get_sweet_sixteen_upset_chance(seed1, seed2):
    """Returns the correct upset chance for Sweet 16 (round 3) matchups"""
    # Higher seed is the one with the lower number
    higher_seed = min(seed1, seed2)
    lower_seed = max(seed1, seed2)
    
    # --------- 1-seed matchups ---------
    if higher_seed == 1:
        if lower_seed in [4, 5]:
            return 33.0  # Updated: changed from 25.0 to 33.0
        elif lower_seed in [12, 13]:
            return 20.0  # Updated: changed from 16.67 to 20.0
        elif lower_seed in [8, 9]:
            return 16.67  # No change
        elif lower_seed == 16:
            return 2.5  # No change
        elif lower_seed in [2, 3]:
            return 50.0  # No change
        elif lower_seed in [6, 7, 10, 11]:
            return 20.0  # No change
        elif lower_seed in [14, 15]:
            return 10.0  # No change
            
    # --------- 2-seed matchups ---------
    elif higher_seed == 2:
        if lower_seed == 3:
            return 50.0  # No change
        elif lower_seed == 6:
            return 33.0  # No change
        elif lower_seed == 11:
            return 25.0  # No change
        elif lower_seed == 14:
            return 25.0  # Updated: changed from 20.0 to 25.0
        elif lower_seed in [7, 10]:
            return 20.0  # No change
        elif lower_seed == 15:
            return 8.33  # No change
        elif lower_seed in [4, 5]:
            return 33.0  # No change
        elif lower_seed in [8, 9]:
            return 25.0  # No change
        elif lower_seed in [12, 13]:
            return 16.67  # No change
        elif lower_seed == 16:
            return 5.0  # No change
            
    # --------- 3-seed matchups ---------
    elif higher_seed == 3:
        if lower_seed == 6:
            return 25.0  # No change
        elif lower_seed == 11:
            return 16.67  # No change
        elif lower_seed == 14:
            return 20.0  # No change
        elif lower_seed == 7:
            return 33.0  # Updated: changed from 25.0 to 33.0
        elif lower_seed == 10:
            return 33.0  # Updated: changed from 25.0 to 33.0
        elif lower_seed == 15:
            return 20.0  # No change
        elif lower_seed in [4, 5]:
            return 50.0  # No change
        elif lower_seed in [8, 9]:
            return 25.0  # No change
        elif lower_seed in [12, 13]:
            return 20.0  # No change
        elif lower_seed == 16:
            return 5.0  # No change
            
    # --------- 4-seed matchups ---------
    elif higher_seed == 4:
        if lower_seed == 5:
            return 50.0  # No change
        elif lower_seed in [12, 13]:
            return 20.0  # No change
        elif lower_seed == 14:
            return 25.0  # No change
        elif lower_seed in [8, 9]:
            return 33.0  # No change
        elif lower_seed == 16:
            return 16.67  # No change
        elif lower_seed in [6, 7, 10, 11]:
            return 25.0  # No change
        elif lower_seed == 15:
            return 16.67  # No change
            
    # --------- 5-seed matchups ---------
    elif higher_seed == 5:
        if lower_seed in [12, 13]:
            return 25.0  # No change
        elif lower_seed in [8, 9]:
            return 33.0  # No change
        elif lower_seed == 16:
            return 16.67  # No change
        elif lower_seed in [6, 7, 10, 11]:
            return 25.0  # No change
        elif lower_seed in [14, 15]:
            return 20.0  # No change
            
    # --------- 6-seed matchups ---------
    elif higher_seed == 6:
        if lower_seed == 7:
            return 50.0  # No change
        elif lower_seed == 10:
            return 33.0  # No change
        elif lower_seed == 11:
            return 33.0  # No change
        elif lower_seed == 14:
            return 25.0  # No change
        elif lower_seed == 15:
            return 25.0  # No change
        elif lower_seed in [8, 9]:
            return 33.0  # No change
        elif lower_seed in [12, 13]:
            return 25.0  # No change
        elif lower_seed == 16:
            return 20.0  # No change
            
    # --------- 7-seed matchups ---------
    elif higher_seed == 7:
        if lower_seed == 10:
            return 33.0  # No change
        elif lower_seed == 11:
            return 33.0  # No change
        elif lower_seed == 14:
            return 25.0  # No change
        elif lower_seed == 15:
            return 16.67  # No change
        elif lower_seed in [8, 9]:
            return 50.0  # No change
        elif lower_seed in [12, 13]:
            return 25.0  # No change
        elif lower_seed == 16:
            return 20.0  # No change
            
    # --------- 8-seed matchups ---------
    elif higher_seed == 8:
        if lower_seed == 9:
            return 50.0  # No change
        elif lower_seed in [12, 13]:
            return 33.0  # No change
        elif lower_seed == 16:
            return 16.67  # No change
        elif lower_seed in [10, 11, 14, 15]:
            return 33.0  # No change
            
    # --------- 9-seed matchups ---------
    elif higher_seed == 9:
        if lower_seed in [12, 13]:
            return 50.0  # No change
        elif lower_seed == 16:
            return 16.67  # No change
        elif lower_seed in [10, 11, 14, 15]:
            return 33.0  # No change
            
    # --------- 10-seed matchups ---------
    elif higher_seed == 10:
        if lower_seed == 11:
            return 50.0  # No change
        elif lower_seed == 14:
            return 33.0  # No change
        elif lower_seed == 15:
            return 33.0  # No change
        elif lower_seed in [12, 13]:
            return 50.0  # No change
        elif lower_seed == 16:
            return 25.0  # No change
            
    # --------- 11-seed matchups ---------
    elif higher_seed == 11:
        if lower_seed == 14:
            return 33.0  # No change
        elif lower_seed == 15:
            return 33.0  # No change
        elif lower_seed in [12, 13]:
            return 50.0  # No change
        elif lower_seed == 16:
            return 25.0  # No change
            
    # --------- 12-seed matchups ---------
    elif higher_seed == 12:
        if lower_seed == 13:
            return 50.0  # No change
        elif lower_seed in [14, 15]:
            return 33.0  # No change
        elif lower_seed == 16:
            return 50.0  # No change
            
    # --------- 13-seed matchups ---------
    elif higher_seed == 13:
        if lower_seed in [14, 15]:
            return 33.0  # No change
        elif lower_seed == 16:
            return 50.0  # No change
            
    # --------- 14-seed matchups ---------
    elif higher_seed == 14:
        if lower_seed == 15:
            return 50.0  # No change
        elif lower_seed == 16:
            return 50.0  # No change
            
    # --------- 15-seed matchups ---------
    elif higher_seed == 15:
        if lower_seed == 16:
            return 50.0  # No change
    
    # Default case
    return 0.0

def get_elite_eight_upset_chance(seed1, seed2):
    """Returns the correct upset chance for Elite Eight (round 4) matchups"""
    # Higher seed is the one with the lower number
    higher_seed = min(seed1, seed2)
    lower_seed = max(seed1, seed2)
    
    # --------- 1-seed matchups ---------
    if higher_seed == 1:
        if lower_seed in [2, 3]:
            return 50.0
        elif lower_seed in [6, 7, 4, 5]:
            return 33.0
        elif lower_seed in [10, 11, 8, 9]:
            return 25.0
        elif lower_seed in [14, 15, 12, 13]:
            return 20.0
        elif lower_seed == 16:
            return 2.5
    
    # --------- 2-seed matchups ---------
    elif higher_seed == 2:
        if lower_seed == 3:
            return 50.0
        elif lower_seed in [4, 5, 6, 7]:
            return 33.0
        elif lower_seed in [8, 9, 10, 11, 14]:
            return 25.0
        elif lower_seed in [12, 13]:
            return 20.0
        elif lower_seed == 15:
            return 20.0
        elif lower_seed == 16:
            return 20.0
    
    # --------- 3-seed matchups ---------
    elif higher_seed == 3:
        if lower_seed == 4:
            return 50.0
        elif lower_seed in [5, 6, 7]:
            return 50.0
        elif lower_seed in [8, 9]:
            return 33.0
        elif lower_seed in [10, 11, 12, 13, 14]:
            return 25.0
        elif lower_seed == 15:
            return 20.0
        elif lower_seed == 16:
            return 20.0
            
    # --------- 4-seed matchups ---------
    elif higher_seed == 4:
        if lower_seed == 5:
            return 50.0
        elif lower_seed in [6, 7]:
            return 33.0
        elif lower_seed in [8, 9, 10]:  # Fixed - added #4 vs #10
            return 33.0
        elif lower_seed == 11:
            return 25.0
        elif lower_seed in [12, 13]:
            return 25.0
        elif lower_seed in [14, 15]:
            return 20.0
        elif lower_seed == 16:
            return 20.0
            
    # --------- 5-seed matchups ---------
    elif higher_seed == 5:
        if lower_seed in [6, 7, 8, 9]:
            return 50.0
        elif lower_seed in [10, 11]:
            return 33.0
        elif lower_seed == 12:
            return 33.0
        elif lower_seed in [13, 14, 15, 16]:
            return 25.0
            
    # --------- 6-seed matchups ---------
    elif higher_seed == 6:
        if lower_seed == 7:
            return 50.0
        elif lower_seed in [8, 9, 10]:
            return 33.0
        elif lower_seed in [11, 12, 13, 14]:
            return 33.0
        elif lower_seed in [15, 16]:
            return 25.0
            
    # --------- 7-seed matchups ---------
    elif higher_seed == 7:
        if lower_seed in [8, 9, 10, 11]:
            return 50.0
        elif lower_seed in [12, 13, 14]:
            return 33.0
        elif lower_seed in [15, 16]:
            return 25.0
            
    # --------- 8-seed matchups ---------
    elif higher_seed == 8:
        if lower_seed == 9:
            return 50.0
        elif lower_seed in [10, 11, 12]:
            return 50.0
        elif lower_seed in [13, 14]:
            return 33.0
        elif lower_seed in [15, 16]:
            return 25.0
            
    # --------- 9-seed matchups ---------
    elif higher_seed == 9:
        if lower_seed in [10, 11, 12]:
            return 50.0
        elif lower_seed in [13, 14]:
            return 33.0
        elif lower_seed in [15, 16]:
            return 25.0
            
    # --------- 10-seed matchups ---------
    elif higher_seed == 10:
        if lower_seed in [11, 12, 13]:
            return 50.0
        elif lower_seed in [14, 15, 16]:
            return 33.0
            
    # --------- 11-seed matchups ---------
    elif higher_seed == 11:
        if lower_seed in [12, 13, 14, 15, 16]:
            return 50.0
            
    # --------- 12-seed matchups ---------
    elif higher_seed == 12:
        if lower_seed in [13, 14, 15, 16]:
            return 50.0
            
    # --------- 13-seed matchups ---------
    elif higher_seed == 13:
        if lower_seed in [14, 15, 16]:
            return 50.0
            
    # --------- 14-seed matchups ---------
    elif higher_seed == 14:
        if lower_seed in [15, 16]:
            return 50.0
            
    # --------- 15-seed matchups ---------
    elif higher_seed == 15:
        if lower_seed == 16:
            return 50.0
    
    # Default case
    return 0.0

def get_final_four_championship_upset_chance(seed1, seed2):
    """Returns the correct upset chance for Final Four and Championship rounds (5-6)"""
    # Higher seed is the one with the lower number
    higher_seed = min(seed1, seed2)
    lower_seed = max(seed1, seed2)
    
    # --------- Implement using ranges for cleaner code ---------
    
    # Seed 1 matchups
    if higher_seed == 1:
        if lower_seed in [1, 2, 3]:
            return 50.0
        elif lower_seed in [4, 5, 6]:
            return 33.0
        elif lower_seed in [7, 8, 9, 10]:
            return 25.0
        elif lower_seed in [11, 12, 13, 14, 15, 16]:
            return 25.0  # Updated from 20.0 to 25.0
    
    # Seed 2 matchups
    elif higher_seed == 2:
        if lower_seed in [2, 3, 4]:
            return 50.0
        elif lower_seed in [5, 6, 7, 8, 9]:
            return 33.0
        elif lower_seed in [10, 11, 12, 13, 14]:
            return 25.0
        elif lower_seed in [15, 16]:
            return 25.0  # Updated from 20.0 to 25.0
    
    # Seed 3 matchups
    elif higher_seed == 3:
        if lower_seed in [3, 4, 5, 6]:
            return 50.0
        elif lower_seed in [7, 8, 9]:
            return 33.0
        elif lower_seed in [10, 11, 12, 13, 14]:
            return 25.0
        elif lower_seed in [15, 16]:
            return 25.0  # Updated from 20.0 to 25.0
    
    # Seed 4 matchups
    elif higher_seed == 4:
        if lower_seed in [4, 5, 6, 7]:
            return 50.0
        elif lower_seed in [8, 9, 10]:
            return 33.0
        elif lower_seed in [11, 12, 13, 14]:
            return 25.0
        elif lower_seed in [15, 16]:
            return 25.0  # Updated from 20.0 to 25.0
    
    # Seed 5 matchups
    elif higher_seed == 5:
        if lower_seed in [5, 6, 7, 8, 9]:
            return 50.0
        elif lower_seed in [10, 11, 12]:
            return 33.0
        elif lower_seed in [13, 14, 15, 16]:
            return 25.0
    
    # Seed 6 matchups
    elif higher_seed == 6:
        if lower_seed in [6, 7, 8, 9, 10]:
            return 50.0
        elif lower_seed in [11, 12, 13, 14]:
            return 33.0
        elif lower_seed in [15, 16]:
            return 25.0
    
    # Seed 7 matchups
    elif higher_seed == 7:
        if lower_seed in [7, 8, 9, 10, 11]:
            return 50.0
        elif lower_seed in [12, 13, 14]:
            return 33.0
        elif lower_seed in [15, 16]:
            return 25.0
    
    # Seed 8 matchups
    elif higher_seed == 8:
        if lower_seed in [8, 9, 10, 11, 12]:
            return 50.0
        elif lower_seed in [13, 14]:
            return 33.0
        elif lower_seed in [15, 16]:
            return 25.0
    
    # Seed 9 matchups
    elif higher_seed == 9:
        if lower_seed in [9, 10, 11, 12]:
            return 50.0
        elif lower_seed in [13, 14]:
            return 33.0
        elif lower_seed in [15, 16]:
            return 25.0
    
    # Seed 10 matchups
    elif higher_seed == 10:
        if lower_seed in [10, 11, 12, 13]:
            return 50.0
        elif lower_seed in [14, 15, 16]:
            return 33.0
    
    # Seed 11 matchups
    elif higher_seed == 11:
        if lower_seed in [11, 12, 13, 14, 15, 16]:
            return 50.0
    
    # Seed 12 matchups
    elif higher_seed == 12:
        if lower_seed in [12, 13, 14, 15, 16]:
            return 50.0
    
    # Seed 13 matchups
    elif higher_seed == 13:
        if lower_seed in [13, 14, 15, 16]:
            return 50.0
    
    # Seed 14 matchups
    elif higher_seed == 14:
        if lower_seed in [14, 15, 16]:
            return 50.0
    
    # Seed 15 matchups
    elif higher_seed == 15:
        if lower_seed in [15, 16]:
            return 50.0
    
    # Seed 16 matchups
    elif higher_seed == 16 and lower_seed == 16:
        return 50.0
    
    # Default case
    return 0.0

# Region names and round names from original code
REGIONS = ["Region A", "Region B", "Region C", "Region D"]

# NCAA tournament round names
ROUND_NAMES = {
    1: "First Round",
    2: "Second Round",
    3: "Sweet Sixteen",
    4: "Elite Eight",
    5: "Final Four",
    6: "National Championship"
}

# ======================== FLASK APP FUNCTIONS ========================

def initialize_game():
    """Initialize or reset the game state"""
    global game_state
    
    # First-round matchups (same as in original code)
    matchups = [
        (1, 16), (8, 9),
        (5, 12), (4, 13),
        (6, 11), (3, 14),
        (7, 10), (2, 15)
    ]
    
    game_state = {
        "current_region_index": 0,
        "current_round": 1,
        "current_matchup_index": 0,
        "regions_completed": 0,
        "champions": [],
        "region_winners": [],
        "round_winners": {
            "Region A": {1: [], 2: [], 3: [], 4: []},
            "Region B": {1: [], 2: [], 3: [], 4: []},
            "Region C": {1: [], 2: [], 3: [], 4: []},
            "Region D": {1: [], 2: [], 3: [], 4: []}
        },
        "final_four_winners": [],
        "matchups": matchups,
        "current_matchup": matchups[0],
        "messages": [
            "╔═══════════════════════════════════════════════╗",
            "║                                               ║",
            "║     NCAA MARCH MADNESS BRACKET SIMULATOR      ║",
            "║                                               ║",
            "╚═══════════════════════════════════════════════╝",
            "",
            "This simulator creates a bracket based on proprietary upset probabilities.",
            "Pick any number when prompted. An upset will occur if your number matches the generated number.",
            "Let's begin!",
            "",
            "===== Starting Region A =====",
            "",
            "Region A - First Round"
        ],
        "waiting_for_input": True,
        "game_over": False,
        "final_four_stage": 0
    }
    
    # Set the first matchup
    game_state["current_matchup"] = game_state["matchups"][0]
    higher_seed, lower_seed = game_state["current_matchup"]
    game_state["messages"].append(f"Matchup: #{higher_seed}-seed vs. #{lower_seed}-seed")

def process_user_choice(user_choice):
    """Process the user's number choice and determine the outcome of the current matchup"""
    global game_state
    
    # Get current matchup information
    seed1, seed2 = game_state["current_matchup"]
    current_round = game_state["current_round"]
    current_region = REGIONS[game_state["current_region_index"]]
    
    # Determine higher and lower seeds
    higher_seed = min(seed1, seed2)
    lower_seed = max(seed1, seed2)
    
    # Get upset chance based on the round
    if current_round == 1:
        upset_chance = get_first_round_upset_chance(seed1, seed2)
    elif current_round == 2:
        upset_chance = get_second_round_upset_chance(seed1, seed2)
    elif current_round == 3:
        upset_chance = get_sweet_sixteen_upset_chance(seed1, seed2)
    elif current_round == 4:
        upset_chance = get_elite_eight_upset_chance(seed1, seed2)
    elif current_round >= 5:  # Final Four and Championship
        upset_chance = get_final_four_championship_upset_chance(seed1, seed2)
    
    # Calculate the target number range based on the upset chance
    # If upset chance is 0, we'll default to 1% chance
    actual_chance = max(1.0, upset_chance)
    chance_denominator = int(100 / actual_chance)
    
    # Generate a dynamic range around the user's number
    # The size of the range is determined by the upset chance
    range_size = chance_denominator
    range_start = max(1, user_choice - range_size // 2)
    
    # Generate a random number within that range
    random_number = random.randint(range_start, range_start + range_size - 1)
    
    # The upset occurs if the random number matches the user's choice
    is_upset = (random_number == user_choice)
    
    # Add messages for the user
    game_state["messages"].append(f"Pick any number: {user_choice}")
    game_state["messages"].append("Determining outcome...")
    
    # Determine winner
    if is_upset:
        winner_seed = lower_seed
        if game_state["final_four_stage"] > 0:
            winner_region = game_state["champions"][seed2-1][1] if seed2 == lower_seed else game_state["champions"][seed1-1][1]
            game_state["messages"].append(f"UPSET! #{lower_seed}-seed ({winner_region}) wins!")
        else:
            game_state["messages"].append(f"UPSET! #{lower_seed}-seed wins!")
    else:
        winner_seed = higher_seed
        if game_state["final_four_stage"] > 0:
            winner_region = game_state["champions"][seed1-1][1] if seed1 == higher_seed else game_state["champions"][seed2-1][1]
            game_state["messages"].append(f"#{higher_seed}-seed ({winner_region}) advances.")
        else:
            game_state["messages"].append(f"#{higher_seed}-seed advances.")
    
    # Handle the winner based on the current stage
    if game_state["final_four_stage"] == 0:
        # Regular region play
        region_key = REGIONS[game_state["current_region_index"]]
        game_state["round_winners"][region_key][current_round].append(winner_seed)
    elif game_state["final_four_stage"] == 1:
        # Final Four - Semifinal 1
        game_state["final_four_winners"].append((winner_seed, winner_region))
        game_state["final_four_stage"] = 2
    elif game_state["final_four_stage"] == 2:
        # Final Four - Semifinal 2
        game_state["final_four_winners"].append((winner_seed, winner_region))
        game_state["final_four_stage"] = 3
    elif game_state["final_four_stage"] == 3:
        # Championship
        game_state["champion"] = (winner_seed, winner_region)
        game_state["game_over"] = True
        game_state["messages"].append(f"🏆 NCAA TOURNAMENT CHAMPION: #{winner_seed}-seed ({winner_region})! 🏆")
    
    # Move to the next matchup
    advance_to_next_matchup()
    
    return winner_seed

def advance_to_next_matchup():
    """Advance to the next matchup in the tournament"""
    global game_state
    
    # If we're in the Final Four/Championship stage
    if game_state["final_four_stage"] > 0:
        if game_state["final_four_stage"] == 1:
            # After Semifinal 1, set up Semifinal 2
            seed1, region1 = game_state["champions"][2]
            seed2, region2 = game_state["champions"][3]
            game_state["current_matchup"] = (seed1, seed2)
            game_state["messages"].append("")
            game_state["messages"].append("Semifinal 2:")
            game_state["messages"].append(f"Matchup: #{seed1}-seed ({region1}) vs. #{seed2}-seed ({region2})")
            game_state["waiting_for_input"] = True
            return
        elif game_state["final_four_stage"] == 2:
            # After Semifinal 2, set up Championship
            seed1, region1 = game_state["final_four_winners"][0]
            seed2, region2 = game_state["final_four_winners"][1]
            game_state["current_matchup"] = (seed1, seed2)
            game_state["messages"].append("")
            game_state["messages"].append("===== NATIONAL CHAMPIONSHIP =====")
            game_state["messages"].append("")
            game_state["messages"].append(f"Matchup: #{seed1}-seed ({region1}) vs. #{seed2}-seed ({region2})")
            game_state["waiting_for_input"] = True
            return
        elif game_state["final_four_stage"] == 3:
            # Game is over
            game_state["waiting_for_input"] = False
            return
    
    # Regular tournament play
    current_region = REGIONS[game_state["current_region_index"]]
    current_round = game_state["current_round"]
    
    # Check if we need to advance to the next matchup in the current round
    if game_state["current_matchup_index"] < len(game_state["matchups"]) - 1:
        game_state["current_matchup_index"] += 1
        game_state["current_matchup"] = game_state["matchups"][game_state["current_matchup_index"]]
        
        # Display the next matchup
        seed1, seed2 = game_state["current_matchup"]
        game_state["messages"].append(f"Matchup: #{seed1}-seed vs. #{seed2}-seed")
        game_state["waiting_for_input"] = True
        return
    
    # If we've completed all matchups in this round
    game_state["current_matchup_index"] = 0
    
    # Check if we need to move to the next round in the current region
    if current_round < 4:  # Still in Rounds 1-3
        # Set up next round's matchups based on winners from this round
        winners = game_state["round_winners"][current_region][current_round]
        new_matchups = []
        
        for i in range(0, len(winners), 2):
            if i + 1 < len(winners):  # Ensure we have pairs
                new_matchups.append((winners[i], winners[i+1]))
        
        game_state["matchups"] = new_matchups
        game_state["current_round"] += 1
        
        # Display the next round header
        game_state["messages"].append("")
        game_state["messages"].append(f"{current_region} - {ROUND_NAMES[game_state['current_round']]}")
        
        # Set up the first matchup of the next round
        game_state["current_matchup"] = new_matchups[0]
        seed1, seed2 = game_state["current_matchup"]
        game_state["messages"].append(f"Matchup: #{seed1}-seed vs. #{seed2}-seed")
        game_state["waiting_for_input"] = True
        return
    
    # If we've completed all rounds in this region
    if current_round == 4:  # Elite Eight completed
        # Store the region champion
        region_champion = game_state["round_winners"][current_region][4][0]
        game_state["champions"].append((region_champion, current_region))
        game_state["messages"].append("")
        game_state["messages"].append(f"{current_region} Champion: #{region_champion}-seed!")
        
        # Move to the next region
        game_state["current_region_index"] += 1
        game_state["regions_completed"] += 1
        
        # Reset for the next region or move to Final Four
        if game_state["current_region_index"] < len(REGIONS):
            # Start the next region
            game_state["current_round"] = 1
            game_state["matchups"] = [
                (1, 16), (8, 9),
                (5, 12), (4, 13),
                (6, 11), (3, 14),
                (7, 10), (2, 15)
            ]
            
            next_region = REGIONS[game_state["current_region_index"]]
            game_state["messages"].append("")
            game_state["messages"].append(f"===== Starting {next_region} =====")
            game_state["messages"].append("")
            game_state["messages"].append(f"{next_region} - {ROUND_NAMES[1]}")
            
            # Set up the first matchup of the next region
            game_state["current_matchup"] = game_state["matchups"][0]
            seed1, seed2 = game_state["current_matchup"]
            game_state["messages"].append(f"Matchup: #{seed1}-seed vs. #{seed2}-seed")
            game_state["waiting_for_input"] = True
            return
        else:
            # All regions completed, move to Final Four
            game_state["current_round"] = 5
            game_state["final_four_stage"] = 1
            
            # Set up Final Four matchups
            game_state["messages"].append("")
            game_state["messages"].append("===== FINAL FOUR =====")
            game_state["messages"].append("")
            game_state["messages"].append("Semifinal 1:")
            
            seed1, region1 = game_state["champions"][0]
            seed2, region2 = game_state["champions"][1]
            game_state["current_matchup"] = (seed1, seed2)
            game_state["messages"].append(f"Matchup: #{seed1}-seed ({region1}) vs. #{seed2}-seed ({region2})")
            game_state["waiting_for_input"] = True
            return

@app.route('/')
def index():
    """Main route to display the simulator"""
    # Reset game state for a new session
    initialize_game()
    return render_template('index.html')

@app.route('/game_state')
def get_game_state():
    """Return the current game state to the client"""
    return jsonify({
        'messages': game_state["messages"],
        'waiting_for_input': game_state["waiting_for_input"],
        'game_over': game_state["game_over"]
    })

@app.route('/submit_number', methods=['POST'])
def submit_number():
    """Process the user's number submission"""
    data = request.get_json()
    user_choice = int(data.get('number', 0))
    
    # No validation limits - allow any number as per original code
    
    # Process the user's choice
    process_user_choice(user_choice)
    
    return jsonify({
        'messages': game_state["messages"],
        'waiting_for_input': game_state["waiting_for_input"],
        'game_over': game_state["game_over"]
    })

if __name__ == '__main__':
    app.run(debug=True)
