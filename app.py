from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# Game state for the bracket simulator
game_state = {
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
        "Region A - First Round",
        "Matchup: #1-seed vs. #16-seed"
    ],
    "waiting_for_input": True,
    "game_over": False
}

@app.route('/')
def index():
    """Main route to display the simulator"""
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
        
        # Add a test response
        game_state["messages"].append(f"Pick any number: {user_choice}")
        game_state["messages"].append("Determining outcome...")
        
        # Determine outcome randomly
        if random.random() < 0.1:  # 10% chance of upset
            game_state["messages"].append(f"UPSET! #16-seed wins!")
        else:
            game_state["messages"].append(f"#1-seed advances.")
        
        game_state["messages"].append("")  # Add blank line after outcome
        game_state["messages"].append("Matchup: #8-seed vs. #9-seed")
        
        return jsonify({
            'messages': game_state["messages"],
            'waiting_for_input': game_state["waiting_for_input"],
            'game_over': game_state["game_over"]
        })
    except Exception as e:
        # Log the error for server-side debugging
        return jsonify({'error': f'Server error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)