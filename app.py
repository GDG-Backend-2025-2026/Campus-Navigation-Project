import os
from flask import Flask
from dotenv import load_dotenv
from models import db 

load_dotenv()

app = Flask(__name__)

# Config
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Initialize the db with the app
db.init_app(app)

# Register Blueprint
from routes.departments import dept_bp
app.register_blueprint(dept_bp)

# Create tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)


   
