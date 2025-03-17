from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    """Main route to display the simulator"""
    return render_template('index.html')

@app.route('/test')
def test():
    """Test route to verify the app is running"""
    return jsonify({
        'status': 'success',
        'message': 'The application is running correctly.'
    })

if __name__ == '__main__':
    app.run(debug=True)