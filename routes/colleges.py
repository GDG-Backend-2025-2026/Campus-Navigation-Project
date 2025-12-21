from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError
from app.extensions import db
from app.models import College

colleges_bp = Blueprint('colleges', __name__)

@colleges_bp.route('/colleges', methods=['GET'])
def get_all_colleges():
    colleges = College.query.all()
    return jsonify([{
        'id': c.id,
        'name': c.name,
        'code': c.code,
        'created_at': c.created_at.isoformat()
    } for c in colleges]), 200

@colleges_bp.route('/colleges/<int:id>', methods=['GET'])
def get_college(id):
    college = College.query.get_or_404(id)
    return jsonify({
        'id': college.id,
        'name': college.name,
        'code': college.code,
        'created_at': college.created_at.isoformat(),
        'updated_at': college.updated_at.isoformat()
    }), 200

@colleges_bp.route('/colleges', methods=['POST'])
@jwt_required()
def create_college():
    data = request.get_json()
    name = data.get('name')
    code = data.get('code')
    
    if not name or not code:
        return jsonify({'message': 'Name and code required'}), 400
    
    try:
        college = College(name=name, code=code)
        db.session.add(college)
        db.session.commit()
        return jsonify({
            'id': college.id,
            'name': college.name,
            'code': college.code,
            'message': 'College created successfully'
        }), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'College name or code already exists'}), 409

@colleges_bp.route('/colleges/<int:id>', methods=['PUT'])
@jwt_required()
def update_college(id):
    college = College.query.get_or_404(id)
    data = request.get_json()
    name = data.get('name', college.name)
    code = data.get('code', college.code)
    
    try:
        college.name = name
        college.code = code
        db.session.commit()
        return jsonify({
            'id': college.id,
            'name': college.name,
            'code': college.code,
            'message': 'College updated successfully'
        }), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'College name or code already exists'}), 409

@colleges_bp.route('/colleges/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_college(id):
    college = College.query.get_or_404(id)
    db.session.delete(college)
    db.session.commit()
    return jsonify({'message': 'College deleted successfully'}), 200
