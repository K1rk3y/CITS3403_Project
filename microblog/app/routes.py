# app/routes.py

from flask import render_template, flash, redirect, url_for, request, jsonify
from app import db
from app.forms import SearchForm, OrderForm
from app.models import Order
from flask import Blueprint
from app.validators import email_validator

bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET', 'POST'])
def submit_order():
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

    return render_template('index.html', form=form)

@bp.route('/orders')
def list_orders():
    orders = Order.query.all()
    for order in orders:
        print(order.first_name, order.last_name, order.email, order.meal)
    return "Orders printed in console"


@bp.route('/search_orders', methods=['GET', 'POST'])
def search_orders():
    form = SearchForm()
    orders = []
    if form.validate_on_submit():
        query = form.query.data.strip().lower()

        orders = Order.query.filter(
            (Order.first_name.ilike(f"%{query}%")) |
            (Order.last_name.ilike(f"%{query}%")) |
            (Order.address.ilike(f"%{query}%")) |
            (Order.suburb.ilike(f"%{query}%")) |
            (Order.phone.ilike(f"%{query}%")) |
            (Order.email.ilike(f"%{query}%")) |
            (Order.meal.ilike(f"%{query}%")) |
            (Order.number_of_people.ilike(f"%{query}%")) |
            (Order.instructions.ilike(f"%{query}%"))
        ).all()

        if not orders:
            flash("No matching orders found.")
        else:
            flash(f"Found {len(orders)} matching orders.")

    return render_template('search_orders.html', form=form, orders=orders)


#Tried elastic search but didnt work, threw errors.
'''
from flask import render_template, flash, redirect, url_for, request, current_app
from app import db
from app.forms import SearchForm, OrderForm
from app.models import Order
from app.search import search_orders  # Import the function from search.py
from flask import Blueprint

bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET', 'POST'])
def submit_order():
    form = OrderForm()
    if form.validate_on_submit():
        order = Order(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            address=form.address.data,
            suburb=form.suburb.data,
            email=form.email.data,
            phone=form.phone.data,
            meal=form.meal.data
        )
        db.session.add(order)
        db.session.commit()
        flash('Order successfully submitted!')
        return redirect(url_for('main.confirmation'))
    return render_template('index.html', form=form)

@bp.route('/confirmation')
def confirmation():
    return render_template('confirmation.html')

@bp.route('/orders')
def list_orders():
    orders = Order.query.all()
    for order in orders:
        print(order.first_name, order.last_name, order.email, order.meal)
    return "Orders printed in console"

@bp.route('/search_orders', methods=['GET', 'POST'], endpoint='search_orders')
def search_orders_route():
    form = SearchForm()
    orders = []
    if form.validate_on_submit():
        query = form.query.data.strip().lower()
        page = request.args.get('page', 1, type=int)

        ids, total = search_orders(query, page, current_app.config['POSTS_PER_PAGE'])
        orders = Order.query.filter(Order.id.in_(ids)).all()

        if not orders:
            flash("No matching orders found.")
        else:
            flash(f"Found {len(orders)} matching orders.")

    return render_template('search_orders.html', form=form, orders=orders)
'''
