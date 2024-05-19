import unittest
from wtforms import Form, StringField, IntegerField, ValidationError
from app.validators import (
    phone_number_validator,
    email_validator,
    address_validator,
    instructions_length_validator,
    number_of_people_validator
)

# Dummy form to use with validators
class DummyForm(Form):
    phone_number = StringField('Phone Number')
    email = StringField('Email')
    address = StringField('Address')
    instructions = StringField('Instructions')
    number_of_people = IntegerField('Number of People')

class TestValidators(unittest.TestCase):

    def setUp(self):
        
        self.form = DummyForm()

    def tearDown(self):
        # Cleanup code 
        pass

    def test_phone_number_validator_valid(self):
        self.form.phone_number.data = "1234567890"
        try:
            phone_number_validator(self.form, self.form.phone_number)
        except ValidationError:
            self.fail("phone_number_validator raised ValidationError unexpectedly!")

    def test_phone_number_validator_invalid(self):
        self.form.phone_number.data = "12345"
        with self.assertRaises(ValidationError):
            phone_number_validator(self.form, self.form.phone_number)

    def test_email_validator_valid(self):
        self.form.email.data = "test@example.com"
        try:
            email_validator(self.form, self.form.email)
        except ValidationError:
            self.fail("email_validator raised ValidationError unexpectedly!")

    def test_email_validator_invalid(self):
        self.form.email.data = "invalid-email"
        with self.assertRaises(ValidationError):
            email_validator(self.form, self.form.email)

    def test_address_validator_valid(self):
        self.form.address.data = "12345 Elm St"
        try:
            address_validator(self.form, self.form.address)
        except ValidationError:
            self.fail("address_validator raised ValidationError unexpectedly!")

    def test_address_validator_invalid(self):
        self.form.address.data = "123"
        with self.assertRaises(ValidationError):
            address_validator(self.form, self.form.address)

    def test_instructions_length_validator_valid(self):
        self.form.instructions.data = "Follow the path"
        try:
            instructions_length_validator(self.form, self.form.instructions)
        except ValidationError:
            self.fail("instructions_length_validator raised ValidationError unexpectedly!")

    def test_instructions_length_validator_invalid(self):
        self.form.instructions.data = "x" * 201
        with self.assertRaises(ValidationError):
            instructions_length_validator(self.form, self.form.instructions)

    def test_number_of_people_validator_valid(self):
        self.form.number_of_people.data = 4
        try:
            number_of_people_validator(self.form, self.form.number_of_people)
        except ValidationError:
            self.fail("number_of_people_validator raised ValidationError unexpectedly!")

    def test_number_of_people_validator_too_few(self):
        self.form.number_of_people.data = 0
        with self.assertRaises(ValidationError):
            number_of_people_validator(self.form, self.form.number_of_people)

    def test_number_of_people_validator_too_many(self):
        self.form.number_of_people.data = 9
        with self.assertRaises(ValidationError):
            number_of_people_validator(self.form, self.form.number_of_people)

if __name__ == '__main__':
    unittest.main()
