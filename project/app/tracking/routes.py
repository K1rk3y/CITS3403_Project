from flask import Blueprint, render_template, session, request
from ..util import record_activity
from .. import db
from ..model import UserActivity

track_bp = Blueprint('tracking', __name__)

@track_bp.route('/activities')
def activities():
    activities = UserActivity.query.order_by(UserActivity.timestamp.desc()).all()
    return render_template('activities.html', activities=activities)