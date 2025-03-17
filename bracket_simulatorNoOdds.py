import random
import time

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

# Region names
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

def play_matchup(seed1, seed2, round_number, region1=None, region2=None):
    """Simulates a matchup based on historical upset odds but with hidden probabilities."""
    # Determine which seed is higher (lower number) and which is lower (higher number)
    higher_seed = min(seed1, seed2)
    lower_seed = max(seed1, seed2)
    
    # Keep track of which input seed is which for correct region assignment
    higher_is_seed1 = (seed1 == higher_seed)
    higher_region = region1 if higher_is_seed1 else region2
    lower_region = region2 if higher_is_seed1 else region1
    
    # Get upset chance based on the round (this is hidden from the user)
    if round_number == 1:
        upset_chance = get_first_round_upset_chance(seed1, seed2)
    elif round_number == 2:
        upset_chance = get_second_round_upset_chance(seed1, seed2)
    elif round_number == 3:
        upset_chance = get_sweet_sixteen_upset_chance(seed1, seed2)
    elif round_number == 4:
        upset_chance = get_elite_eight_upset_chance(seed1, seed2)
    elif round_number >= 5:  # Final Four and Championship
        upset_chance = get_final_four_championship_upset_chance(seed1, seed2)
    
    # Display matchup info without showing probabilities
    if round_number >= 5 and region1 and region2:
        print(f"\nMatchup: #{higher_seed}-seed ({higher_region}) vs. #{lower_seed}-seed ({lower_region})")
    else:
        print(f"\nMatchup: #{higher_seed}-seed vs. #{lower_seed}-seed")
    
    # Calculate the target number range based on the upset chance
    # If upset chance is 0, we'll default to 1% chance
    actual_chance = max(1.0, upset_chance)
    chance_denominator = int(100 / actual_chance)
    
    # Ask the user to pick any number
    user_choice = int(input("Pick any number: "))
    
    # Generate a dynamic range around the user's number
    # The size of the range is determined by the upset chance
    range_size = chance_denominator
    range_start = max(1, user_choice - range_size // 2)
    
    # Generate a random number within that range
    random_number = random.randint(range_start, range_start + range_size - 1)
    
    # The upset occurs if the random number matches the user's choice
    is_upset = (random_number == user_choice)
    
    # The random number is no longer displayed to the user
    # Just a small pause for effect
    print("Determining outcome...\n")
    time.sleep(0.5)
    
    # Determine winner and include region information for Final Four and Championship
    if is_upset:
        if round_number >= 5 and region1 and region2:
            winner_seed = lower_seed
            winner_region = lower_region
            print(f"UPSET! #{lower_seed}-seed ({winner_region}) wins!\n")
            return lower_seed, winner_region
        else:
            print(f"UPSET! #{lower_seed}-seed wins!\n")
            return lower_seed
    else:
        if round_number >= 5 and region1 and region2:
            winner_seed = higher_seed
            winner_region = higher_region
            print(f"#{higher_seed}-seed ({winner_region}) advances.\n")
            return higher_seed, winner_region
        else:
            print(f"#{higher_seed}-seed advances.\n")
            return higher_seed

def simulate_region(region_name, matchups):
    """Simulates an entire region round by round."""
    print(f"\n===== Starting {region_name} =====\n")
    
    # First Round
    print(f"{region_name} - {ROUND_NAMES[1]}")
    
    winners = []
    for seed1, seed2 in matchups:
        winner = play_matchup(seed1, seed2, 1)
        winners.append(winner)
    
    round_number = 2
    while len(winners) > 1:
        # Use round name if available, otherwise use "Round X"
        round_display = ROUND_NAMES.get(round_number, f"Round {round_number}")
        print(f"\n{region_name} - {round_display}")
        
        next_round = []
        for i in range(0, len(winners), 2):
            winner = play_matchup(winners[i], winners[i+1], round_number)
            next_round.append(winner)
        
        winners = next_round
        round_number += 1
    
    # Return both the seed and the region name
    print(f"\n{region_name} Champion: #{winners[0]}-seed!")
    return winners[0], region_name

def main():
    print("""
    ╔═══════════════════════════════════════════════╗
    ║                                               ║
    ║     NCAA MARCH MADNESS BRACKET SIMULATOR      ║
    ║                                               ║
    ╚═══════════════════════════════════════════════╝
    """)
    
    print("This simulator creates a bracket based on proprietary upset probabilities.")
    print("Pick any number when prompted. An upset will occur if your number matches the generated number.")
    print("\nLet's begin!\n")
    
    # First-round matchups - explicitly ordered as higher seed first, lower seed second
    matchups = [
        (1, 16), (8, 9),
        (5, 12), (4, 13),
        (6, 11), (3, 14),
        (7, 10), (2, 15)
    ]
    
    # Store both the seed and region for each champion
    champions = [simulate_region(region, matchups) for region in REGIONS]
    
    # Final Four - Round 5
    print("\n===== FINAL FOUR =====\n")
    
    # Unpack the champions list to separate seeds and regions
    seeds = [champ[0] for champ in champions]
    regions = [champ[1] for champ in champions]
    
    # Play Final Four matchups with region identifiers
    print("Semifinal 1:")
    final_matchup1 = play_matchup(seeds[0], seeds[1], 5, regions[0], regions[1])
    
    print("Semifinal 2:")
    final_matchup2 = play_matchup(seeds[2], seeds[3], 5, regions[2], regions[3])
    
    # Championship - Round 6
    print("\n===== NATIONAL CHAMPIONSHIP =====\n")
    
    # Unpack the semifinal winners
    finalist1_seed, finalist1_region = final_matchup1
    finalist2_seed, finalist2_region = final_matchup2
    
    # Play championship with region identifiers
    champion_seed, champion_region = play_matchup(finalist1_seed, finalist2_seed, 6, finalist1_region, finalist2_region)
    
    print(f"\n🏆 NCAA TOURNAMENT CHAMPION: #{champion_seed}-seed ({champion_region})! 🏆\n")

if __name__ == "__main__":
    main()