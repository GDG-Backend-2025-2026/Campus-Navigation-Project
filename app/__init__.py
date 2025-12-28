from flask import Flask
from flask_migrate import Migrate
from config import Config
from utils.db import db  # Use the SAME db instance as routes/models

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    # Import models BEFORE create_all() - use models/ package (same as routes use)
    from models import Building, User

    # Create tables if they don't exist
    with app.app_context():
        db.create_all()

    # Register blueprints
    from routes import register_blueprints
    register_blueprints(app)

    return app
