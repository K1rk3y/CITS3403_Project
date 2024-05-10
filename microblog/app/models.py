# app/models.py
from app import db

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(128), nullable=False)
    suburb = db.Column(db.String(64))
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    meal = db.Column(db.String(64), nullable=False)
    number_of_people = db.Column(db.Integer, nullable=False)
    instructions = db.Column(db.String(200))

