import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from app import create_app, db
from app.model import User
from werkzeug.security import generate_password_hash

class SeleniumTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('TestConfig')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create a unique test user
        self.test_username = 'testuser_{}'.format(hash(self))
        user = User(username=self.test_username, password=generate_password_hash('testpassword'), email='test@example.com')
        db.session.add(user)
        db.session.commit()

        # Specify the correct chromedriver path if needed
        self.driver = webdriver.Chrome(executable_path='/test3/project/chrome-linux64')

    def tearDown(self):
        self.driver.quit()
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_login(self):
        driver = self.driver
        driver.get('http://localhost:5001/login-patron')

        # Find the login form elements
        username_input = driver.find_element_by_name('username')
        password_input = driver.find_element_by_name('password')
        submit_button = driver.find_element_by_name('submit')

        # Fill out the form and submit
        username_input.send_keys(self.test_username)
        password_input.send_keys('testpassword')
        submit_button.click()

        # Check if login was successful
        self.assertIn('Logged in successfully', driver.page_source)

    def test_registration(self):
        driver = self.driver
        driver.get('http://localhost:5001/register')

        # Find the registration form elements
        username_input = driver.find_element_by_name('username')
        email_input = driver.find_element_by_name('email')
        password_input = driver.find_element_by_name('password')
        confirm_password_input = driver.find_element_by_name('confirm')
        role_select = driver.find_element_by_name('role')
        submit_button = driver.find_element_by_name('submit')

        # Fill out the form and submit
        username_input.send_keys('newuser')
        email_input.send_keys('newuser@example.com')
        password_input.send_keys('newpassword')
        confirm_password_input.send_keys('newpassword')
        role_select.send_keys('Patron')
        submit_button.click()

        # Check if registration was successful
        self.assertIn('Your account has been created!', driver.page_source)

    def test_order_submission(self):
        driver = self.driver
        driver.get('http://localhost:5001/login-patron')

        # Log in first
        username_input = driver.find_element_by_name('username')
        password_input = driver.find_element_by_name('password')
        submit_button = driver.find_element_by_name('submit')
        username_input.send_keys(self.test_username)
        password_input.send_keys('testpassword')
        submit_button.click()

        # Navigate to order form
        driver.get('http://localhost:5001/requests')

        # Find the order form elements
        first_name_input = driver.find_element_by_name('first_name')
        last_name_input = driver.find_element_by_name('last_name')
        address_input = driver.find_element_by_name('address')
        suburb_input = driver.find_element_by_name('suburb')
        email_input = driver.find_element_by_name('email')
        phone_input = driver.find_element_by_name('phone')
        meal_select = driver.find_element_by_name('meal')
        number_of_people_input = driver.find_element_by_name('number_of_people')
        instructions_input = driver.find_element_by_name('instructions')
        submit_button = driver.find_element_by_name('submit')

        # Fill out the form and submit
        first_name_input.send_keys('John')
        last_name_input.send_keys('Doe')
        address_input.send_keys('123 Main St')
        suburb_input.send_keys('Anytown')
        email_input.send_keys('john.doe@example.com')
        phone_input.send_keys('1234567890')
        meal_select.send_keys('Vegan')
        number_of_people_input.send_keys('4')
        instructions_input.send_keys('Please deliver between 6-7 PM.')
        submit_button.click()

        # Check if order submission was successful
        self.assertIn('Order successfully submitted!', driver.page_source)

if __name__ == "__main__":
    unittest.main()
