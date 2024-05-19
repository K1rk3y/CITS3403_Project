Description of the purpose of the application

This application provides a interactive platform for two parties of users, one known as "Home cook" and the other known as "Patrons". The Patrons may create and submit custom meal orders onto the website, and teh Home cooks may respond to those orders. It utilizes the Flask framework along with Flask-WTF for form handling form inputs and validation, and it provides a user-friendly interface for users to input their order details, and a powerful search function which returns details about a user order, or any order related queries in general using a built in AI assistant. Here are the details of this application:

Users can login, register as two different roles, and logout via accounts handled by Flask and sqlite db models, access to certain webpages are restricted to logged in sessions only. 
The request and search pages are access controlled by the account system.
Users can create and submit a form handled by Flask-WTF which may contain the details of their custom meal orders.
Users can search for orders and their details using a search function powered by sqlite db models.
Users can ask any order related general queries via the same search bar, which will be answered by an AI search assistant powered by GPT-4o and context embedding based prompt engineering.
All fields in login, signup, submit meal request are validated by validators that are either built in on teh client side JS or handled by Flask Form validators to ensure proper format.
JavaScripts are used throughout the application for beautification and graphics for ease of interaction / visual appeals.


Group members

| Name | Student ID | Github username |
|----------|----------|----------|
| Cheng Li    | 23468614   | K1rk3y   |
|   Nishk Patel   | 23363009   | Nishk139   |
| Sreelajoyoti Mitra    | 23297983   | Sreelajoyoti  |
| Amadea Yinata   | Data 5   | ayin2830  |



Instructions for how to launch the application
1. install all prerequisites
2. move the project folder to WSL environment
3. fill in the OpenAI API key in ai_core.py
4. run "run.py"
5. access http://localhost:5000/home


List of prerequisites

pip install flask
pip install flask_login
pip install flask_sqlalchemy
pip install pandas
pip install tiktoken
pip install openai
pip install numpy
pip install scipy
pip install flask_wtf
pip install flask_migrate
pip install email_validator
pip install selenium
pip install flask-testing


Instructions for how to run the tests for the application



