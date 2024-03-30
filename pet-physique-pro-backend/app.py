""" Flask app """
from flask import Flask, render_template, request, session, redirect, url_for
from api.db import db # Import Database setup
from api.models import ma
from api.models import User
from api.blueprint import app_views
import os
from flask_cors import CORS  # Import the CORS module
from flask_bcrypt import Bcrypt  # Import bcrypt for pswd hashing
from flask import jsonify



app = Flask(__name__)
app.secret_key = 'PetPhysique' # for session management


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
"""nitialize bcrypt"""
bcrypt = Bcrypt(app)


"""home page"""
@app.route('/')
def home():
    return render_template("home.html")

"""sign in"""
@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        # get user data from login form
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if username/email and password are provided
        if not username or not password:
            return render_template("login.html", error='Missing username/email or password')

        # Query the database for the user
        user = User.query.filter((User.username == username) | (User.email == username)).first()

        # Check if user exists and password is correct
        if user and bcrypt.check_password_hash(user.password, password):
            # Store user's ID in session
            session['user_id'] = user.id
            session['username'] = user.username
            session['email'] = user.email
            # Redirect to dashboard or profile page
            return redirect(url_for('dashboard.html'))
        else:
            return render_template('login.html', error='Invalid username/email or password')

    # If method is GET, render the login form
    return render_template('login.html')



"""sign up"""
@app.route('/sign-up', methods=["POST", "GET"])
def signin():
    if request.method == "POST":
        # Get data from request
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # if username/email already exists render login page
        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            return render_template('login.html', error='User already exists. Please log in.')

        # If not, reate a new user
        new_user = User(username=username, email=email, password=bcrypt.generate_password_hash(password).decode('utf-8'))
        db.session.add(new_user)
        db.session.commit()

        # Store user's ID in session
        session['user_id'] = new_user.id

        # Redirect to dashboard (We have to change this to profile page)
        return redirect(url_for('home'))

    else:
        return render_template("signup.html")
    
"""sign out"""
@app.route('/logout')
def logout():
    # clear user session
    session.clear()
    return redirect(url_for('home'))

from api.models import Pet

@app.route('/dashboard')
def dashboard():
    # Check if user is logged in
    if 'user_id' in session:
        # Retrieve user data from session
        user_id = session['user_id']
        username = session['username']
        email = session['email']
        # Query database for pets associated with the user
        user_pets = Pet.query.filter_by(user_id=user_id).all()
        # Render dashboard template with user information and pets
        return render_template("dashboard.html", current_user={'user_id': user_id, 'username': username, 'email': email}, user_pets=user_pets)
    else:
        # Redirect to login page if user is not logged in
        return redirect(url_for('login'))

# Route to handle requests for user information
@app.route('/user-info')
def get_user_info():
    # Retrieve user information from session or database
    user_info = {
        'username': session.get('username'),
        'email': session.get('email'),
        'user_id': session.get('user_id')
    }
    # Return user information as JSON response
    return jsonify(user_info)

@app.route('/pet-info')
def get_pet_info():
    # Retrieve pet information from the database
    pets = Pet.query.all()
    # Convert pet objects to a list of dictionaries
    pet_info = [{
        'name': pet.name,
        'id': session.get('user_id'),
        'type': pet.type,
        'age': pet.age,
        'height': pet.height,
        'weight': pet.weight
    } for pet in pets]
    # Return pet information as JSON response
    return jsonify(pet_info)

"""create pet page"""
@app.route('/create_pet')
def create_pet_page():
    return render_template('create_pet.html')

"""About us page"""
@app.route('/about-us')
def about_us():
    return render_template('about_us.html')

@app.route('/update_pet/<int:pet_id>')
def update_pet_page(pet_id):
    return render_template('update_pet.html', pet_id=pet_id)

# Run the Flask app
if __name__ == '__main__':
     # Importing db here ensures it's imported within the application context.
    from app import db
    # Create the database tables based on the defined models
    with app.app_context():
        db.create_all()
    app.run(debug=True)
