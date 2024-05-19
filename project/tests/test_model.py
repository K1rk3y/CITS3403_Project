import unittest
from app import create_app, db
from app.model import User, Order
from flask_testing import TestCase
from werkzeug.security import generate_password_hash

class OrderUpdateTestCase(TestCase):

    def create_app(self):
        return create_app('TestConfig')

    def setUp(self):
        """Set up test environment"""
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

            # Create a test user
            user = User(username='testuser', password=generate_password_hash('testpassword'), email='test@example.com')
            db.session.add(user)
            db.session.commit()

            # Log in the user
            response = self.client.post('/login-patron', data=dict(
                username='testuser',
                password='testpassword'
            ), follow_redirects=True)
            print("Login response status code:", response.status_code)
            print("Login response data:", response.data.decode())
            self.assertEqual(response.status_code, 200, "Login failed")

    def tearDown(self):
        """Tear down test environment"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_order_update(self):
        """Test that an existing order is updated with new data"""
        with self.app.app_context():
            # Create and submit the initial order
            initial_order_data = {
                'first_name': 'Jim',
                'last_name': 'Hal',
                'address': '123 abc Street',
                'suburb': 'Test Suburb',
                'email': 'Jim.Hal@example.com',
                'phone': '1234567890',
                'meal': 'vegan',
                'number_of_people': 4,
                'instructions': 'No onions'
            }
            response = self.client.post('/requests', data=initial_order_data, follow_redirects=True)
            print("Initial order response status code:", response.status_code)
            print("Initial order response data:", response.data.decode())
            self.assertEqual(response.status_code, 200)

            # Check that the order was created
            order = Order.query.filter_by(email='john.doe@example.com').first()
            self.assertIsNotNone(order, "Initial order creation failed")
            self.assertEqual(order.first_name, 'John')

            # Submit updated order data
            updated_order_data = {
                'first_name': 'Jane',
                'last_name': 'Smith',
                'address': '456 Oak Street',
                'suburb': 'New Suburb',
                'email': 'john.doe@example.com',  # same email to update the order
                'phone': '0987654321',
                'meal': 'vegetarian',
                'number_of_people': 2,
                'instructions': 'Extra sauce'
            }
            response = self.client.post('/requests', data=updated_order_data, follow_redirects=True)
            print("Updated order response status code:", response.status_code)
            print("Updated order response data:", response.data.decode())
            self.assertEqual(response.status_code, 200)

            # Check that the existing order was updated
            order = Order.query.filter_by(email='john.doe@example.com').first()
            self.assertIsNotNone(order, "Order update failed")
            self.assertEqual(order.first_name, 'Jane')
            self.assertEqual(order.last_name, 'Smith')
            self.assertEqual(order.address, '456 Oak Street')
            self.assertEqual(order.suburb, 'New Suburb')
            self.assertEqual(order.phone, '0987654321')
            self.assertEqual(order.meal, 'vegetarian')
            self.assertEqual(order.number_of_people, 2)
            self.assertEqual(order.instructions, 'Extra sauce')

if __name__ == '__main__':
    unittest.main()
