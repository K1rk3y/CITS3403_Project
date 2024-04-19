from flask import Blueprint

submit_bp = Blueprint('submit', __name__)

@submit_bp.route('/submit')
def dashboard():
    return 'submit page'
