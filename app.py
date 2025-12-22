
from flask import Flask, render_template
from config import Config
from models import *
from routes import register_blueprints
from utils.db import db
from dotenv import load_dotenv
import os

load_dotenv()
def create_app():
    """
    Create and configure the Flask app, register blueprints, and initialize extensions.
    """
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config.from_object(Config)
    # Use SQLite for testing if DATABASE_URL is not set
    basedir = os.path.abspath(os.path.dirname(__file__))
    os.makedirs(basedir+"\instance",exist_ok=True)
    #because on mac it uses \ I used os.path.join to access database
    if not os.environ.get('DATABASE_URL'):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,"instance",'test.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    register_blueprints(app)

    @app.route('/')
    def index():
        """Serve the main UI page."""
        return render_template('index.html')

    return app

if __name__ == "__main__":
    app = create_app()
    # Create tables if using SQLite for demo/testing
    with app.app_context():
        db.create_all()
    app.run(debug=True)
