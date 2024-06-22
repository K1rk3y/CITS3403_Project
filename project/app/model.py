from . import db
from datetime import datetime, timezone
from flask_login import UserMixin

class UserActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    path = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    # Implementing the required methods and properties for Flask-Login
    def get_id(self):
        return str(self.id)

    @property
    def is_authenticated(self):
        # Define your logic for user authentication here, e.g., check if the user is authenticated
        return True  # For example, always return True if authentication is not implemented

    @property
    def is_active(self):
        # Define your logic to determine if the user is active or not
        return True  # For example, always return True if all users are considered active

    @property
    def is_anonymous(self):
        return False  # Assuming users are not anonymous in your system