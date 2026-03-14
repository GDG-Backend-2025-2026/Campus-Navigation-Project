from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from flasgger import Swagger
from config import Config
from utils.db import db  # Use the SAME db instance as routes/models
from swagger import swagger_template, swagger_config

migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)  # Allow CORS for all origins
    
    # Initialize Swagger
    Swagger(app, template=swagger_template, config=swagger_config)

    # Import models BEFORE create_all() - use models/ package (same as routes use)
    from models import Building, User, Route, RouteCard

    # Create tables if they don't exist
    with app.app_context():
        db.create_all()

    # Register blueprints
    from routes import register_blueprints
    register_blueprints(app)

    return app
