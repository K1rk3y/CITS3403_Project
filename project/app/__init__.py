from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    
    db.init_app(app)

    with app.app_context():
        from . import model  # Import models
        db.create_all()      # Create database tables

    from .auth.routes import auth_bp
    from .form.routes import form_bp
    from .submit.routes import submit_bp
    from .tracking.routes import track_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(form_bp)
    app.register_blueprint(submit_bp)
    app.register_blueprint(track_bp)

    return app