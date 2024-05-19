from wtforms import ValidationError

# Validator for phone numbers
def phone_number_validator(form, field):
    phone_number = field.data
    if len(phone_number) != 10 or not phone_number.isdigit():
        raise ValidationError('Invalid phone number. Must contain exactly 10 digits.')

# Validator for email addresses
def email_validator(form, field):
    email = field.data
    if not '@' in email or '.' not in email.split('@')[-1]:
        raise ValidationError('Invalid email address format.')

# Validator for addresses
def address_validator(form, field):
    address = field.data
    if len(address.strip()) < 5:
        raise ValidationError('Address should contain at least 5 characters.')

# Validator for instructions length
def instructions_length_validator(form, field):
    instructions = field.data
    if len(instructions) > 200:
        raise ValidationError('Special instructions should not exceed 200 characters.')

# Validator for number of people
def number_of_people_validator(form, field):
    number = field.data
    min_people = 1
    max_people = 8

    if number < min_people or number > max_people:
        raise ValidationError(f'Invalid number of people. Must be between {min_people} and {max_people}.')
