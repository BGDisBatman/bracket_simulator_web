from flask import Flask, render_template, request
import bracket_simulatorNoOdds  # Import your script

app = Flask(__name__)

# Route for the homepage (where users enter their data)
@app.route('/')
def home():
    return render_template('index.html')  # This is the form page

# Route to handle running the script (user submits data)
@app.route('/run_script', methods=['POST'])
def run_script():
    input_data = request.form['input_data']  # Get the data from the form
    # Call your script function with the input data
    result = bracket_simulatorNoOdds.simulate(input_data)  # Assuming you have a function 'simulate' in your script
    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
