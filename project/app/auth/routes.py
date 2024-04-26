from flask import Blueprint, render_template, session, request, flash, redirect, url_for
from ..util import record_activity
from ..form_class import LoginForm, RegistrationForm
from werkzeug.security import check_password_hash, generate_password_hash
from ..model import UserActivity, User
from .. import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and check_password_hash(user.password, form.password.data):
                session['user_id'] = user.id  # Store user's ID in session
                session['username'] = form.username.data  # Set username in session
                flash('Logged in successfully', 'success')
                return redirect(url_for('auth.login_success'))
            else:
                flash('Invalid username or password', 'error')
    return render_template('login.html', title='Sign In', form=form)


@auth_bp.route('/login_success')
def login_success():
    if 'username' in session and 'user_id' in session:
        return f"Welcome {session['username']}! Login successful."
    return redirect(url_for('auth.login'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if 'username' in session and 'user_id' in session:
        return f"{session['username']}, you are already logged in. Log out to register."
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=generate_password_hash(form.password.data))
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('auth.login'))  # Assuming the login route is named 'subfolder.login'
    return render_template('register.html', title='Register', form=form)


@auth_bp.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))