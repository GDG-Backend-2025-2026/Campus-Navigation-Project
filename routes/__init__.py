# routes/__init__.py

from .buildings import buildings_bp
# from .colleges import colleges_bp
# from .departments import departments_bp
# from .lecturers import lecturers_bp
from .routes import routes_bp
from .route_card import route_card_bp
from .auth import auth_bp

def register_blueprints(app):
    """
    Register all blueprints to the Flask app.
    """
    app.register_blueprint(buildings_bp)
    # app.register_blueprint(colleges_bp)
    # app.register_blueprint(departments_bp)
    # app.register_blueprint(lecturers_bp)
    app.register_blueprint(routes_bp)
    app.register_blueprint(route_card_bp)
    app.register_blueprint(auth_bp)
