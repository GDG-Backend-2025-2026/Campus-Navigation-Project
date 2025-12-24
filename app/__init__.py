import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

# Import extensions after app creation
from .extensions import db, jwt

def create_app():
    app = Flask(__name__)
    
    # Load environment variables
    load_dotenv()
    
    # Config from env
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET')
    
    # Init extensions
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)
    
    # Register blueprints
    from routes.colleges import colleges_bp
    from routes.auth import auth_bp
    app.register_blueprint(colleges_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/api')
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    @app.route('/')
    def home():
        return {'message': 'Campus Navigation API - Colleges Management'}
    
    return app
