from flask import Blueprint, render_template, session, request, flash, redirect, url_for, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from ..form_class import LoginForm, RegistrationForm
from ..model import UserActivity, User
from .. import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login')
def login():
    return render_template('login.html', title='Sign In')


@auth_bp.route('/login-cook', methods=['GET', 'POST'])
def login_cook():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)  # Log in the user
            flash('Logged in successfully', 'success')
            return redirect(url_for('form.index'))
    else:
        flash('Invalid username or password', 'error')
    return render_template('login-cook.html', title='Sign In', form=form)


@auth_bp.route('/login-patron', methods=['GET', 'POST'])
def login_patron():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)  # Log in the user
            flash('Logged in successfully', 'success')
            return redirect(url_for('form.index'))
    else:
        flash('Invalid username or password', 'error')
    return render_template('login-patron.html', title='Sign In', form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return render_template('logout.html', title='Sign Out', logout_message = "You are already logged in, logout to continue.", confirm_text = "Log Out", cancel_text = 'Cancel')
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=generate_password_hash(form.password.data))
        db.session.add(user)
        db.session.commit()
        flash_message = 'Your account has been created! You are now able to log in'
        flash(flash_message, 'success')
        return redirect(url_for('auth.login'))  # Redirect to the login page after successful registration
    
    return render_template('sign-up.html', title='Register', form=form, flash_message=None)


@auth_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    action = request.form.get('action')
    if action == 'confirm':
        # Handle confirm action
        logout_user()
        return redirect(url_for('form.index'))
    elif action == 'cancel':
        # Handle cancel action
        return redirect(url_for('form.index'))

    # If the request method is GET or the user navigates to /logout directly
    return render_template('logout.html', title='Sign Out', logout_message="Are you sure you want to log out?", confirm_text="Log Out", cancel_text='Cancel')