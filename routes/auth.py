from flask import Blueprint, request, jsonify
from utils.auth import encode_auth_token
from utils.db import db
from models import User
from utils.auth import jwt_required

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Dummy user for demonstration
ADMIN_USER = {'username': 'admin', 'password': 'admin123'}

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or data.get('username') != ADMIN_USER['username'] or data.get('password') != ADMIN_USER['password']:
        return jsonify({'message': 'Invalid credentials'}), 401
    token = encode_auth_token(ADMIN_USER['username'])
    return jsonify({'token': token})
@auth_bp.route('/signup', methods=['POST'])
@jw
def signup():
    data = request.get_json()
    if not data or data.get('username') :
        return jsonify({'message': 'Enter valid data'}), 404
    user = User(name = data["name"])
    db.session.add(user)
    db.session.commit()
    token = encode_auth_token(ADMIN_USER['username'])
    return jsonify({'token': token})