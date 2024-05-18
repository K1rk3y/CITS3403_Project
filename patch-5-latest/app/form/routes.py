from flask import Blueprint, render_template, session, request, flash, redirect, url_for, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from ..form_class import SearchForm, OrderForm
from ..model import UserActivity, User, Order
from app.validators import email_validator
from .. import db

form_bp = Blueprint('form', __name__)

@form_bp.route('/home')
def index():
    return render_template('index.html')


@form_bp.route('/about')
def about_us():
    return render_template('about-us.html')

@form_bp.route('/requests', methods=['GET', 'POST'])
def submit_order():
    if not current_user.is_authenticated:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('auth.login_patron'))
    form = OrderForm()
    if form.validate_on_submit():
        existing_order = Order.query.filter_by(email=form.email.data).first()
        if existing_order:
            # Update the existing order with new data
            existing_order.first_name = form.first_name.data
            existing_order.last_name = form.last_name.data
            existing_order.address = form.address.data
            existing_order.suburb = form.suburb.data
            existing_order.phone = form.phone.data
            existing_order.meal = form.meal.data
            existing_order.number_of_people = form.number_of_people.data
            existing_order.instructions = form.instructions.data
            flash('Order successfully updated!')
        else:
            # Create a new order if no existing order is found
            order = Order(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                address=form.address.data,
                suburb=form.suburb.data,
                email=form.email.data,
                phone=form.phone.data,
                meal=form.meal.data,
                number_of_people=form.number_of_people.data,
                instructions=form.instructions.data
            )
            db.session.add(order)
            flash('Order successfully submitted!')
        
        db.session.commit()
        # Return a JSON response indicating success
        return jsonify({'message': 'Order placed successfully'})

    return render_template('requests.html', form=form)

@form_bp.route('/list_orders')
def list_orders():
    orders = Order.query.all()
    for order in orders:
        print(order.first_name, order.last_name, order.email, order.meal)
    return "Orders printed in console"


@form_bp.route('/discussion', methods=['GET', 'POST'])
def search_orders():
    if not current_user.is_authenticated:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('auth.login_patron'))
    form = SearchForm()
    orders = []
    if form.validate_on_submit():
        query = form.query.data.strip().lower() if form.query.data else ''
        mealType = form.mealType.data.strip().lower() if form.mealType.data else ''
        numOfMeals = form.numOfMeals.data if form.numOfMeals.data else None
        suburb = form.suburb.data.strip().lower() if form.suburb.data else ''

        filters = []

        if query:
            filters.append(
                (Order.first_name.ilike(f"%{query}%")) |
                (Order.last_name.ilike(f"%{query}%")) |
                (Order.address.ilike(f"%{query}%")) |
                (Order.suburb.ilike(f"%{query}%")) |
                (Order.phone.ilike(f"%{query}%")) |
                (Order.email.ilike(f"%{query}%")) |
                (Order.meal.ilike(f"%{query}%")) |
                (Order.instructions.ilike(f"%{query}%"))
            )

        if mealType:
            filters.append(Order.meal.ilike(f"%{mealType}%"))

        if numOfMeals is not None:
            filters.append(Order.number_of_people == numOfMeals)

        if suburb:
            filters.append(Order.suburb.ilike(f"%{suburb}%"))

        if filters:
            orders = Order.query.filter(*filters).all()

        if not orders:
            flash("No matching orders found.")
        else:
            flash(f"Found {len(orders)} matching orders.")

    return render_template('search_orders.html', form=form, orders=orders)
    