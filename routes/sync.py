from flask import Blueprint, jsonify
from models import Building, Route, RouteCard

sync_bp = Blueprint('sync', __name__)


@sync_bp.route('/all', methods=['GET'])
def get_all_data():
    """
    Get All Data for Offline Sync
    ---
    tags:
      - Sync
    responses:
      200:
        description: All data for offline use
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            data:
              type: object
              properties:
                buildings:
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: integer
                      name:
                        type: string
                      image_url:
                        type: string
                      description:
                        type: string
                routes:
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: integer
                      start_building_id:
                        type: integer
                      end_building_id:
                        type: integer
                steps:
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: integer
                      route_id:
                        type: integer
                      step_number:
                        type: integer
                      instruction:
                        type: string
                      image_url:
                        type: string
    """
    buildings = Building.query.all()
    routes = Route.query.all()
    steps = RouteCard.query.all()
    
    return jsonify({
        'success': True,
        'data': {
            'buildings': [
                {
                    'id': b.id,
                    'name': b.name,
                    'image_url': b.image_url,
                    'description': b.description
                } for b in buildings
            ],
            'routes': [
                {
                    'id': r.id,
                    'start_building_id': r.start_building_id,
                    'end_building_id': r.end_building_id
                } for r in routes
            ],
            'steps': [
                {
                    'id': s.id,
                    'route_id': s.route_id,
                    'step_number': s.step_number,
                    'instruction': s.instruction,
                    'image_url': s.image_url
                } for s in steps
            ]
        }
    })
