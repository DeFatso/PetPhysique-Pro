from flask import request, jsonify
from api.db import db  # Import Database setup
from api.models import UserSchema, User
from api.blueprint import app_views


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
@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    data = request.json
    if 'username' not in data or 'email' not in data:
        return jsonify({"error": "Missing username or email"}), 400

    username = data['username']
    email = data['email']

    new_user = User(username=username, email=email)
    db.session.add(new_user)
    db.session.commit()

    user_schema = UserSchema()
    return jsonify(user_schema.dump(new_user)), 201


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
