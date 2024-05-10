from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Email
from app.validators import phone_number_validator, address_validator, instructions_length_validator, number_of_people_validator

class OrderForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired(), address_validator])
    suburb = StringField('Suburb', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired(), phone_number_validator])
    meal = SelectField('Meal', choices=[
        ('normal', 'Normal'), ('vegan', 'Vegan'),
        ('vegetarian', 'Vegetarian'), ('pescatarian', 'Pescatarian'),
        ('nut-free', 'Nut-Free')
    ], validators=[DataRequired()])
    number_of_people = IntegerField('Number of People', validators=[DataRequired(), number_of_people_validator])
    instructions = TextAreaField('Special Instructions', validators=[instructions_length_validator])
    submit = SubmitField('Submit')


class SearchForm(FlaskForm):
    query = StringField('Search Orders', validators=[DataRequired()])
    submit = SubmitField('Search')