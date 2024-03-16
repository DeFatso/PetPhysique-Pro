""" Flask app """
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS  # Import the CORS module

app = Flask(__name__)
CORS(app)

"""home page"""
@app.route('/')
def home():
    return render_template("home.html")

"""sign in"""
@app.route('/login')
def login():
    return render_template("login.html")

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
