""" Flask app """
from flask import Flask, render_template
from api.db import db # Import Database setup
from api.models import ma
from api.blueprint import app_views
import os
from flask_cors import CORS  # Import the CORS module

app = Flask(__name__)

"""Database configuration"""
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')

"""Sqlalchemy track modification"""
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

"""Initialize db"""
db.init_app(app)
"""Initialize marshmallow"""
ma.init_app(app)
"""Register blueprint"""
app.register_blueprint(app_views)
"""implement cors to all origin"""
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


"""home page"""
@app.route('/')
def home():
    return render_template("home.html")

"""sign in"""
@app.route('/login')
def login():
    return render_template("login.html")

"""sign up"""
@app.route('/sign-up')
def signin():
    return render_template("signin.html")

# Run the Flask app
if __name__ == '__main__':
     # Importing db here ensures it's imported within the application context.
    from app import db
    # Create the database tables based on the defined models
    with app.app_context():
        db.create_all()
    app.run(debug=True)
