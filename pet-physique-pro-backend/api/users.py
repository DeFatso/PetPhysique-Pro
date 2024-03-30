from flask import redirect, request, jsonify, session, url_for
from api.db import db  # Import Database setup
from flask_bcrypt import Bcrypt
from api.models import UserSchema, PetSchema, User, Pet
from api.blueprint import app_views

bcrypt = Bcrypt()

"""Get all recorded users"""
@app_views.route("/users", methods=["GET"], strict_slashes=False)
def get_users():
    users = User.query.all()
    user_schema = UserSchema(many=True)
    return jsonify(user_schema.dump(users))


"""Get a single user"""
@app_views.route("/users/<int:user_id>", methods=["GET"], strict_slashes=False)
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        user_schema = UserSchema()
        return jsonify(user_schema.dump(user)), 200
    else:
        return jsonify({"error": "User not found"}), 404


"""Create a new user"""
@app_views.route("/signup", methods=["POST"], strict_slashes=False)
def create_user():
    data = request.json
    if 'username' not in data or 'email' not in data:
        return jsonify({"error": "Missing username or email"}), 400

    username = data['username']
    email = data['email']
    password = data['password']

    """Check if email already exist in the database"""
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({"error": "Email already exist, Login instead"})

    new_user = User(username=username, email=email, password=bcrypt.generate_password_hash(password).decode('utf-8'))
    db.session.add(new_user)
    db.session.commit()

    # Check if pets data is provided in the request
    if 'pets' in data:
        pets_data = data['pets']
        for pet_data in pets_data:
            name = pet_data.get('name')
            type = pet_data.get('type')
            weight = pet_data.get('weight')
            height = pet_data.get('height')
            age = pet_data.get('age')
            
            # Create a new pet associated with the user
            new_pet = Pet(type=type, weight=weight, height=height, age=age, user_id=new_user.id)
            db.session.add(new_pet)
        db.session.commit()

    user_schema = UserSchema()
    return jsonify(user_schema.dump(new_user)), 201


"""Login existingUser"""
@app_views.route("/login", methods=["POST"], strict_slashes=False)
def login_user():
    data = request.json
    
    if "email" not in data or "password" not in data:
        return jsonify({"error": "Missing email or password"}), 400
    
    email = data["email"]
    password = data["password"]
    """Fetch user by email from database"""
    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        # Create a session for the user
        session['user_id'] = user.id
        session['username'] = user.username
        session['email'] = user.email
        # Redirect the user to the dashboard
        return redirect(url_for('dashboard'))
    else:
        return jsonify({"error": "Invalid email or password"}, 401)



"""Update an existing user"""
@app_views.route("/users/<int:user_id>", methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    user = User.query.get(user_id)
    if not user: # user doesn't exist, exit gracefully
        return jsonify({"error": "User not found"}), 404

    data = request.json
    if "username" not in data and "email" not in data:
        return jsonify({"error": "No data provided for update"}), 400

    if "username" in data:
        user.username = data["username"]

    if "email" in data:
        user.email = data["email"]

    db.session.commit()
    user_schema = UserSchema()
    return jsonify(user_schema.dump(user))


"""Delete an existing user"""
@app_views.route("/users/<int:user_id>", methods=["DELETE"], strict_slashes=False)
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user: # user doesn't exist, exit gracefully
        return jsonify({"error": "User not found"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"})


"""Get all pets associated with a specific user"""
@app_views.route("/users/<int:user_id>/pets", methods=["GET"], strict_slashes=False)
def get_user_pets(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404

    # Access the 'pets' attribute of the user object to get all pets associated with the user
    user_pets = user.pets

    # Serialize the user pets
    pet_schema = PetSchema(many=True)
    result = pet_schema.dump(user_pets)

    return jsonify(result), 200
