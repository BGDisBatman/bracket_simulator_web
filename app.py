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
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data received'}), 400
            
        # Try to get the number from the request
        if 'number' not in data:
            return jsonify({'error': 'No number provided'}), 400
            
        try:
            user_choice = int(data.get('number', 0))
        except ValueError:
            return jsonify({'error': 'Invalid number format'}), 400
        
        # No validation limits - allow any number as per original code
        
        # Process the user's choice
        process_user_choice(user_choice)
        
        return jsonify({
            'messages': game_state["messages"],
            'waiting_for_input': game_state["waiting_for_input"],
            'game_over': game_state["game_over"]
        })
    except Exception as e:
        # Log the error for server-side debugging
        app.logger.error(f"Error processing number: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
