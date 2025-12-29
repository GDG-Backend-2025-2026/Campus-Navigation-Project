from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.models import (
        building,
        college,
        department,
        lecturer,
        route,
        route_card,
        admin
    )

    # Register blueprints
    from app.routes.offline_sync import offline_sync_bp
    app.register_blueprint(offline_sync_bp)

    return app
