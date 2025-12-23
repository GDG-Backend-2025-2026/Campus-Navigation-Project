from flask import Blueprint, request, jsonify
from utils.auth import jwt_required

route_card_bp = Blueprint('route_card', __name__, url_prefix='/route-cards')
route_cards = []

@route_card_bp.route('/', methods=['GET'])
def get_route_cards():
    """Get all route cards."""
    return jsonify(route_cards)

@route_card_bp.route('/', methods=['POST'])
@jwt_required
def create_route_card():
    """Create a new route card (admin only)."""
    data = request.get_json()
    card = {'id': len(route_cards) + 1, 'name': data['name']}
    route_cards.append(card)
    return jsonify(card), 201
