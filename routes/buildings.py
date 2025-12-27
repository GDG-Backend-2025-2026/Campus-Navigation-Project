from flask import Blueprint, request, jsonify
from models.building import Building
from utils.db import db
from utils.auth import jwt_required

buildings_bp = Blueprint('buildings', __name__, url_prefix='/buildings')

@buildings_bp.route('/', methods=['GET'])
def get_buildings():
    """Get all buildings."""
    buildings = Building.query.all()
    return jsonify([{'id': b.id, 'name': b.name} for b in buildings])

@buildings_bp.route('/<int:id>', methods=['GET'])
def get_building(id):
    """Get a single building by ID."""
    building = Building.query.get_or_404(id)
    return jsonify({'id': building.id, 'name': building.name})

@buildings_bp.route('/', methods=['POST'])
@jwt_required
def create_building():
    """Create a new building (admin only)."""
    data = request.get_json()
    building = Building(name=data['name'])
    db.session.add(building)
    db.session.commit()
    return jsonify({'id': building.id, 'name': building.name}), 201

@buildings_bp.route('/<int:id>', methods=['PUT'])
@jwt_required
def update_building(id):
    """Update a building (admin only)."""
    building = Building.query.get_or_404(id)
    data = request.get_json()
    building.name = data.get('name', building.name)
    db.session.commit()
    return jsonify({'id': building.id, 'name': building.name})

@buildings_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required
def delete_building(id):
    """Delete a building (admin only)."""
    building = Building.query.get_or_404(id)
    db.session.delete(building)
    db.session.commit()
    return jsonify({'message': 'Building deleted'})
