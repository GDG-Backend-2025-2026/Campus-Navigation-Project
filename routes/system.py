from flask import Blueprint, jsonify
from models import Building, Route

system_bp = Blueprint('system', __name__)


@system_bp.route('/overview', methods=['GET'])
def get_overview():
    """
    System Overview Stats
    ---
    tags:
      - System
    responses:
      200:
        description: System statistics
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            data:
              type: object
              properties:
                total_buildings:
                  type: integer
                  example: 12
                total_routes:
                  type: integer
                  example: 8
    """
    total_buildings = Building.query.count()
    total_routes = Route.query.count()
    
    return jsonify({
        'success': True,
        'data': {
            'total_buildings': total_buildings,
            'total_routes': total_routes
        }
    })
