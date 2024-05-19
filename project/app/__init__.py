from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_name='Config'):
    app = Flask(__name__)
    app.config.from_object(f'config.{config_name}')


'''def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False'''
    
    db.init_app(app)
    login_manager.init_app(app)
    migrate = Migrate(app, db)

    with app.app_context():
        from . import model  # Import models
        db.create_all()      # Create database tables

    from .auth.routes import auth_bp
    from .form.routes import form_bp
    from .submit.routes import submit_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(form_bp)
    app.register_blueprint(submit_bp)

    from .model import User  # Import your User model

    @login_manager.user_loader
    def load_user(user_id):
        # Load and return the User object
        return User.query.get(int(user_id))

    return app
