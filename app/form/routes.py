from flask import Blueprint

form_bp = Blueprint('form', __name__)

@form_bp.route('/')
def index():
    return 'form homepage'

@form_bp.route('/post/<int:post_id>')
def post(post_id):
    return f'Viewing post {post_id}'
