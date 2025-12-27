from flask import Blueprint, request, jsonify
from utils.auth import jwt_required

routes_bp = Blueprint('routes', __name__, url_prefix='/routes')
routes = []

@routes_bp.route('/', methods=['GET'])
def get_routes():
    """Get all routes."""
    return jsonify(routes)

@routes_bp.route('/', methods=['POST'])
@jwt_required
def create_route():
    """Create a new route (admin only)."""
    data = request.get_json()
    route = {'id': len(routes) + 1, 'name': data['name']}
    routes.append(route)
    return jsonify(route), 201
