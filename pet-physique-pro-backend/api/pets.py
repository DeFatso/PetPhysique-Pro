from flask import request, jsonify
from api.db import db # Import Database setup
from api.models import PetSchema, Pet, User
from api.blueprint import app_views


"""Get all pets route"""
@app_views.route("/pets", methods=["GET"], strict_slashes=False)
def get_pets():
    pet = Pet.query.all()
    user_schema = PetSchema(many=True)
    return jsonify(user_schema.dump(pet))

"""Create pet route"""
@app_views.route("/pets", methods=["POST"], strict_slashes=False)
def create_pet():
    data = request.json

    if 'type' not in data or 'weight' not in data or 'height' not in data or 'age' not in data or 'user_id' not in data or 'name' not in data:
        return jsonify({"error": "Missing name or type or weight or height or age or user"}), 400
    
    user_id = data.get("user_id")
    if user_id is None:
        return jsonify({"message": "User ID not provided"}), 400
    
    """Check if user exist in db"""
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"message": "User Not Found"}), 404
    
    name = data['name']
    type = data['type']
    weight = data['weight']
    height = data['height']
    age = data['age']

    
    new_pet = Pet(name=name, type=type, weight=weight, height=height, age=age, user_id=user_id)
    db.session.add(new_pet)
    db.session.commit()
    
    pet_schema = PetSchema()
    return jsonify(pet_schema.dump(new_pet)), 201

"""Update pet route"""
@app_views.route("/pets/<int:pet_id>", methods=["PUT"], strict_slashes=False)
def update_pet(pet_id):
    pet = Pet.query.get(pet_id)
    if not pet:
        return jsonify({"error": "Pet not found"}), 404
    data = request.json
    if "type" not in data and "weight" not in data and "height" not in data and "age" not in data and "name" not in data:
        return jsonify({"error": "No data provided for update"}), 400
    if "name" in data:
        pet.name = data["name"]
    if "type" in data:
        pet.type = data["type"]
    if "weight" in data:
        pet.weight = data["weight"]
    if "height" in data:
        pet.height = data["height"]
    if "age" in data:
        pet.age = data["age"]
    db.session.commit()
    pet_schema = PetSchema()
    return jsonify(pet_schema.dump(pet))

"""Delete pet route"""
@app_views.route("/pets/<int:pet_id>", methods=["DELETE"], strict_slashes=False)
def delete_pet(pet_id):
    pet = Pet.query.get(pet_id)
    if not pet:
        return jsonify({"error": "Pet not found"}), 404
    db.session.delete(pet)
    db.session.commit()
    return jsonify({"message": "Pet deleted successfully"})
