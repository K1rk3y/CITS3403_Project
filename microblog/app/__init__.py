from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from elasticsearch import Elasticsearch
from config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initializing SQLAlchemy
    db.init_app(app)
    
    # Initializing Flask-Migrate
    migrate.init_app(app, db)
    
    '''
    # Initializing Elasticsearch with error handling (Removing since doesnt work)
    try:
        app.elasticsearch = Elasticsearch(app.config['ELASTICSEARCH_URL'])
    except Exception as e:
        app.logger.error("Failed to initialize Elasticsearch: %s", e)

    if not app.elasticsearch.indices.exists(index="orders"):
        app.elasticsearch.indices.create(index="orders")
    '''
    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app

