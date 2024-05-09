# app/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired

class OrderForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    suburb = StringField('Suburb')
    email = StringField('Email', validators=[DataRequired()])
    phone = StringField('Phone')
    meal = SelectField('Meal', choices=[
        ('normal', 'Normal'), ('vegan', 'Vegan'),
        ('vegetarian', 'Vegetarian'), ('pescatarian', 'Pescatarian'),
        ('nut-free', 'Nut-Free')
    ])
    submit = SubmitField('Submit')

class SearchForm(FlaskForm):
    query = StringField('Search Orders', validators=[DataRequired()])
    submit = SubmitField('Search')