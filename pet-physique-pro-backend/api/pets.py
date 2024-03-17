from flask import request, jsonify
from api.db import db # Import Database setup
from api.models import PetSchema, Pet
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
    if 'type' not in data or 'weight' not in data or 'height' not in data:
        return jsonify({"error": "Missing type or weight or height"}), 400
    
    type = data['type']
    weight = data['weight']
    height = data['height']
    
    new_pet = Pet(type=type, weight=weight, height=height)
    db.session.add(new_pet)
    db.session.commit()
    
    pet_schema = PetSchema()
    return jsonify(pet_schema.dump(new_pet)), 201