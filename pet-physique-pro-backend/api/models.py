from api.db import db
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
ma = Marshmallow()

"""Define Pet model"""
class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Float, nullable=False)
    age = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class PetSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Pet

"""The User model"""
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False) # only hashed pswd is stored
    pets = db.relationship('Pet', backref='owner', lazy=True)

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        """ ignore password when instantiating"""
        # exclude = ['password_hash']



