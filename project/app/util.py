from flask import session, request
from . import db
from .model import UserActivity


def record_activity():
    if 'username' not in session:
        # You should replace this with actual user session management
        session['username'] = request.remote_addr  # Example placeholder

    activity = UserActivity(user_id=session['username'], path=request.path)
    db.session.add(activity)
    db.session.commit()
