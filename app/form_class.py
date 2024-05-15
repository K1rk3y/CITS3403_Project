from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError, SelectField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length, Email
from app.validators import phone_number_validator, address_validator, instructions_length_validator, number_of_people_validator


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6),
        EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        from app.model import User  # Import here to avoid circular imports
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken. Please choose a different one.')
        

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