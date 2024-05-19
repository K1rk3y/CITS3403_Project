import unittest
from app import create_app, db
from app.model import Order
from app.form.routes import process_order_logic
import random

class ProcessOrderLogicLargeDBTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('TestConfig')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

        with self.app_context:
            db.create_all()

        self.form_data = {
            'email': 'jim.hal@example.com',
            'first_name': 'Jim',
            'last_name': 'Hal',
            'address': '123 Elm St',
            'suburb': 'Suburbia',
            'phone': '1234567890',
            'meal': 'Pizza',
            'number_of_people': 2,
            'instructions': 'Extra cheese'
        }

        # Populate the database with a large number of varied entries
        self.populate_large_database()

    def tearDown(self):
        with self.app_context:
            db.session.remove()
            db.drop_all()
        self.app_context.pop()

    def populate_large_database(self):
        large_number = 10000  # Adjust this number as needed to simulate a large database
        meal_options = ['Pizza', 'Vegan', 'Vegetarian', 'Pescatarian', 'Nut-Free']
        instructions_options = ['Extra cheese', 'No onions', 'Gluten-free', 'Extra sauce', 'No garlic']

        orders = [
            Order(
                email=f'user{i}@example.com',
                first_name=f'FirstName{i}',
                last_name=f'LastName{i}',
                address=f'Address{i}',
                suburb=f'Suburb{i}',
                phone=f'{random.randint(1000000000, 9999999999)}',
                meal=random.choice(meal_options),
                number_of_people=random.randint(1, 10),
                instructions=random.choice(instructions_options)
            )
            for i in range(large_number)
        ]
        db.session.bulk_save_objects(orders)
        db.session.commit()

    def test_process_order_logic_with_large_db_create_new(self):
        with self.app_context:
            response = process_order_logic(self.form_data, Order, db.session)
            self.assertEqual(response['message'], 'Order successfully submitted!')

            order = Order.query.filter_by(email=self.form_data['email']).first()
            self.assertIsNotNone(order)
            self.assertEqual(order.first_name, self.form_data['first_name'])

    def test_process_order_logic_with_large_db_update_existing(self):
        with self.app_context:
            # Insert an existing order
            existing_order = Order(
                email=self.form_data['email'],
                first_name='OldFirstName',
                last_name='OldLastName',
                address='Old Address',
                suburb='OldSuburb',
                phone='0000000000',
                meal='OldMeal',
                number_of_people=1,
                instructions='Old instructions'
            )
            db.session.add(existing_order)
            db.session.commit()

            response = process_order_logic(self.form_data, Order, db.session)
            self.assertEqual(response['message'], 'Order successfully updated!')

            order = Order.query.filter_by(email=self.form_data['email']).first()
            self.assertIsNotNone(order)
            self.assertEqual(order.first_name, self.form_data['first_name'])
            self.assertEqual(order.last_name, self.form_data['last_name'])
            self.assertEqual(order.address, self.form_data['address'])
            self.assertEqual(order.suburb, self.form_data['suburb'])
            self.assertEqual(order.phone, self.form_data['phone'])
            self.assertEqual(order.meal, self.form_data['meal'])
            self.assertEqual(order.number_of_people, self.form_data['number_of_people'])
            self.assertEqual(order.instructions, self.form_data['instructions'])

if __name__ == '__main__':
    unittest.main()
