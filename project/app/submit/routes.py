from flask import Blueprint, render_template, session, request
from ..util import record_activity

submit_bp = Blueprint('submit', __name__)

@submit_bp.route('/submit')
def dashboard():
    record_activity()
    return 'submit page'
