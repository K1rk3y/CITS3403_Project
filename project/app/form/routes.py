from flask import Blueprint, render_template, session, request, flash, redirect, url_for, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from ..form_class import SearchForm, OrderForm
from ..model import UserActivity, User
from app.validators import email_validator
from .. import db

form_bp = Blueprint('form', __name__)

@form_bp.route('/home')
def index():
    return render_template('index.html')


@form_bp.route('/about')
def about_us():
    return render_template('about-us.html')
    
    