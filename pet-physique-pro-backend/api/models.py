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


class PetSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Pet
