# routes/__init__.py

from .buildings import buildings_bp
from .routes import routes_bp
from .auth import auth_bp
from .system import system_bp
from .sync import sync_bp


def register_blueprints(app):
    """
    Register all blueprints to the Flask app under /api/v1.
    """
    app.register_blueprint(buildings_bp, url_prefix='/api/v1/buildings')
    app.register_blueprint(routes_bp, url_prefix='/api/v1/routes')
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(system_bp, url_prefix='/api/v1/system')
    app.register_blueprint(sync_bp, url_prefix='/api/v1/sync')
