from flask import Blueprint, request, jsonify
from utils.auth import encode_auth_token
from utils.db import db
from models import User
from utils.auth import jwt_required

auth_bp = Blueprint('auth', __name__)

# Dummy user for demonstration
ADMIN_USER = {'username': 'admin', 'password': 'admin123'}


@auth_bp.route('/login/', methods=['POST'])
def login():
    """
    Admin Login
    ---
    tags:
      - Authentication
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
              example: admin
            password:
              type: string
              example: admin123
    responses:
      200:
        description: Login successful
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            token:
              type: string
              example: jwt_token_here
      401:
        description: Invalid credentials
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            message:
              type: string
              example: Invalid credentials
    """
    data = request.get_json()
    if not data or data.get('username') != ADMIN_USER['username'] or data.get('password') != ADMIN_USER['password']:
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
    token = encode_auth_token(ADMIN_USER['username'])
    return jsonify({'success': True, 'token': token})


@auth_bp.route('/signup', methods=['POST'])
@jwt_required
def signup():
    """
    User Signup (Admin only)
    ---
    tags:
      - Authentication
    security:
      - BearerAuth: []
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - name
          properties:
            name:
              type: string
              example: John Doe
    responses:
      200:
        description: Signup successful
        schema:
          type: object
          properties:
            token:
              type: string
      404:
        description: Invalid data
    """
    data = request.get_json()
    if not data or data.get('username'):
        return jsonify({'message': 'Enter valid data'}), 404
    user = User(name=data["name"])
    db.session.add(user)
    db.session.commit()
    token = encode_auth_token(ADMIN_USER['username'])
    return jsonify({'token': token})
