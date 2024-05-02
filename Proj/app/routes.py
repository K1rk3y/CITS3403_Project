from flask import render_template, redirect, url_for, flash, request
from app import db
from app.forms import OrderForm
from app.models import Order
from flask import Blueprint

bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():
    form = OrderForm()
    if form.validate_on_submit():
        order = Order(first_name=form.first_name.data, last_name=form.last_name.data,
                      address=form.address.data, suburb=form.suburb.data,
                      email=form.email.data, phone=form.phone.data, meal=form.meal.data)
        db.session.add(order)
        db.session.commit()
        flash('Order successfully submitted!')
        return redirect(url_for('main.confirmation'))
    return render_template('index.html', form=form)

@bp.route('/confirmation')
def confirmation():
    return render_template('confirmation.html')
