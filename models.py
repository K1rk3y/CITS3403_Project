from app import db

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=True, nullable=False)
    last_name = db.Column(db.String(64), index=True, nullable=False)
    address = db.Column(db.String(128)) #mention this as an issue
    suburb = db.Column(db.String(64))
    email = db.Column(db.String(120), index=True, nullable=False)
    phone = db.Column(db.String(20))
    meal = db.Column(db.String(50))
