import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from app import create_app, db
from app.form_class import LoginForm, RegistrationForm
from app.model import User

class TestForms(unittest.TestCase):
    def setUp(self):
        # Create a Flask app context for testing
        self.app = create_app('TestConfig')
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Create all tables
        with self.app_context:
            db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # LoginForm Tests
    def test_login_form_valid(self):
        form = LoginForm(data={'username': 'testuser', 'password': 'testpassword'})
        self.assertTrue(form.validate())

    def test_login_form_invalid_missing_username(self):
        form = LoginForm(data={'username': '', 'password': 'testpassword'})
        self.assertFalse(form.validate())

    def test_login_form_invalid_missing_password(self):
        form = LoginForm(data={'username': 'testuser', 'password': ''})
        self.assertFalse(form.validate())

    # RegistrationForm Tests
    @patch('app.model.User.query.filter_by')
    def test_registration_form_valid(self, mock_user_query):
        mock_user_query.return_value.first.return_value = None
        form = RegistrationForm(data={
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'testpassword',
            'confirm': 'testpassword',
            'role': 'Homecook'
        })
        self.assertTrue(form.validate())

    @patch('app.model.User.query.filter_by')
    def test_registration_form_invalid_missing_email(self, mock_user_query):
        mock_user_query.return_value.first.return_value = None
        form = RegistrationForm(data={
            'email': '',
            'username': 'testuser',
            'password': 'testpassword',
            'confirm': 'testpassword',
            'role': 'Homecook'
        })
        self.assertFalse(form.validate())

    @patch('app.model.User.query.filter_by')
    def test_registration_form_invalid_missing_username(self, mock_user_query):
        mock_user_query.return_value.first.return_value = None
        form = RegistrationForm(data={
            'email': 'test@example.com',
            'username': '',
            'password': 'testpassword',
            'confirm': 'testpassword',
            'role': 'Homecook'
        })
        self.assertFalse(form.validate())

    @patch('app.model.User.query.filter_by')
    def test_registration_form_invalid_missing_password(self, mock_user_query):
        mock_user_query.return_value.first.return_value = None
        form = RegistrationForm(data={
            'email': 'test@example.com',
            'username': 'testuser',
            'password': '',
            'confirm': 'testpassword',
            'role': 'Homecook'
        })
        self.assertFalse(form.validate())

    @patch('app.model.User.query.filter_by')
    def test_registration_form_invalid_password_mismatch(self, mock_user_query):
        mock_user_query.return_value.first.return_value = None
        form = RegistrationForm(data={
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'testpassword',
            'confirm': 'differentpassword',
            'role': 'Homecook'
        })
        self.assertFalse(form.validate())

    @patch('app.model.User.query.filter_by')
    def test_registration_form_invalid_missing_role(self, mock_user_query):
        mock_user_query.return_value.first.return_value = None
        form = RegistrationForm(data={
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'testpassword',
            'confirm': 'testpassword',
            'role': ''
        })
        self.assertFalse(form.validate())

if __name__ == '__main__':
    unittest.main()
