import json
from flask import Blueprint, request, jsonify
from models import Route, RouteCard, Building
from utils.db import db
from utils.auth import jwt_required
from utils.cloudinary import upload_image

routes_bp = Blueprint('routes', __name__)


@routes_bp.route('', methods=['GET'])
def get_routes():
    """
    Get All Routes
    ---
    tags:
      - Routes
    responses:
      200:
        description: List of all routes
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            data:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    example: 5
                  start_building:
                    type: string
                    example: Main Gate
                  end_building:
                    type: string
                    example: Engineering Block
    """
    routes = Route.query.all()
    
    return jsonify({
        'success': True,
        'data': [
            {
                'id': r.id,
                'start_building': r.start_building.name if r.start_building else None,
                'end_building': r.end_building.name if r.end_building else None
            } for r in routes
        ]
    })


@routes_bp.route('/<int:id>', methods=['GET'])
def get_route(id):
    """
    Get Route Details
    ---
    tags:
      - Routes
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: Route ID
    responses:
      200:
        description: Route details with steps
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            data:
              type: object
              properties:
                route_id:
                  type: integer
                  example: 5
                start_building:
                  type: object
                  properties:
                    id:
                      type: integer
                      example: 1
                    name:
                      type: string
                      example: Main Gate
                end_building:
                  type: object
                  properties:
                    id:
                      type: integer
                      example: 3
                    name:
                      type: string
                      example: Engineering Block
                steps:
                  type: array
                  items:
                    type: object
                    properties:
                      step_number:
                        type: integer
                        example: 1
                      instruction:
                        type: string
                        example: Walk straight
                      image_url:
                        type: string
                        example: https://image.com/step1.jpg
      404:
        description: Route not found
    """
    route = Route.query.get(id)
    if not route:
        return jsonify({'success': False, 'message': 'Resource not found'}), 404
    
    # Sort steps by step_number
    sorted_steps = sorted(route.steps, key=lambda s: s.step_number)
    
    return jsonify({
        'success': True,
        'data': {
            'route_id': route.id,
            'start_building': {
                'id': route.start_building.id,
                'name': route.start_building.name
            } if route.start_building else None,
            'end_building': {
                'id': route.end_building.id,
                'name': route.end_building.name
            } if route.end_building else None,
            'steps': [
                {
                    'step_number': s.step_number,
                    'instruction': s.instruction,
                    'image_url': s.image_url
                } for s in sorted_steps
            ]
        }
    })


@routes_bp.route('', methods=['POST'])
@jwt_required
def create_route():
    """
    Create Route (Admin)
    ---
    tags:
      - Routes
    security:
      - BearerAuth: []
    consumes:
      - multipart/form-data
    parameters:
      - name: start_building_id
        in: formData
        type: integer
        required: true
        description: Starting building ID
      - name: end_building_id
        in: formData
        type: integer
        required: true
        description: Destination building ID
      - name: steps
        in: formData
        type: string
        required: false
        description: JSON array of steps [{step_number, instruction}]
      - name: step_image_0
        in: formData
        type: file
        required: false
        description: Image for step 0
      - name: step_image_1
        in: formData
        type: file
        required: false
        description: Image for step 1
    responses:
      201:
        description: Route created
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            route_id:
              type: integer
              example: 5
      400:
        description: Invalid input
      404:
        description: Building not found
      401:
        description: Unauthorized
    """
    # Get form data
    start_building_id = request.form.get('start_building_id', type=int)
    end_building_id = request.form.get('end_building_id', type=int)
    steps_json = request.form.get('steps', '[]')
    
    if not start_building_id or not end_building_id:
        return jsonify({'success': False, 'message': 'Invalid input'}), 400
    
    # Parse steps JSON
    try:
        steps_data = json.loads(steps_json)
    except json.JSONDecodeError:
        return jsonify({'success': False, 'message': 'Invalid input'}), 400
    
    # Verify buildings exist
    start_building = Building.query.get(start_building_id)
    end_building = Building.query.get(end_building_id)
    if not start_building or not end_building:
        return jsonify({'success': False, 'message': 'Resource not found'}), 404
    
    # Create route
    route = Route(
        start_building_id=start_building_id,
        end_building_id=end_building_id
    )
    db.session.add(route)
    db.session.flush()  # Get the route ID
    
    # Create steps with image uploads
    for i, step_data in enumerate(steps_data):
        image_url = None
        
        # Check for step image file (step_image_0, step_image_1, etc.)
        image_key = f'step_image_{i}'
        if image_key in request.files:
            image_file = request.files[image_key]
            if image_file.filename:
                upload_result = upload_image(image_file, folder="campus-navigation/routes")
                if upload_result['success']:
                    image_url = upload_result['url']
        
        step = RouteCard(
            route_id=route.id,
            step_number=step_data.get('step_number', i + 1),
            instruction=step_data.get('instruction', ''),
            image_url=image_url
        )
        db.session.add(step)
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'route_id': route.id
    }), 201


@routes_bp.route('/<int:id>', methods=['PUT'])
@jwt_required
def update_route(id):
    """
    Update Route (Admin)
    ---
    tags:
      - Routes
    security:
      - BearerAuth: []
    consumes:
      - multipart/form-data
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: Route ID
      - name: start_building_id
        in: formData
        type: integer
        required: false
        description: New starting building ID
      - name: end_building_id
        in: formData
        type: integer
        required: false
        description: New destination building ID
      - name: steps
        in: formData
        type: string
        required: false
        description: JSON array of steps (replaces all existing steps)
      - name: step_image_0
        in: formData
        type: file
        required: false
        description: Image for step 0
    responses:
      200:
        description: Route updated
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: Route updated
      404:
        description: Route or building not found
      401:
        description: Unauthorized
    """
    route = Route.query.get(id)
    if not route:
        return jsonify({'success': False, 'message': 'Resource not found'}), 404
    
    # Get form data
    start_building_id = request.form.get('start_building_id', type=int)
    end_building_id = request.form.get('end_building_id', type=int)
    steps_json = request.form.get('steps')
    
    if start_building_id:
        building = Building.query.get(start_building_id)
        if not building:
            return jsonify({'success': False, 'message': 'Resource not found'}), 404
        route.start_building_id = start_building_id
    
    if end_building_id:
        building = Building.query.get(end_building_id)
        if not building:
            return jsonify({'success': False, 'message': 'Resource not found'}), 404
        route.end_building_id = end_building_id
    
    # Update steps if provided
    if steps_json:
        try:
            steps_data = json.loads(steps_json)
        except json.JSONDecodeError:
            return jsonify({'success': False, 'message': 'Invalid input'}), 400
        
        # Remove existing steps
        RouteCard.query.filter_by(route_id=route.id).delete()
        
        # Add new steps with image uploads
        for i, step_data in enumerate(steps_data):
            image_url = None
            
            # Check for step image file
            image_key = f'step_image_{i}'
            if image_key in request.files:
                image_file = request.files[image_key]
                if image_file.filename:
                    upload_result = upload_image(image_file, folder="campus-navigation/routes")
                    if upload_result['success']:
                        image_url = upload_result['url']
            
            step = RouteCard(
                route_id=route.id,
                step_number=step_data.get('step_number', i + 1),
                instruction=step_data.get('instruction', ''),
                image_url=image_url
            )
            db.session.add(step)
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Route updated'
    })


@routes_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required
def delete_route(id):
    """
    Delete Route (Admin)
    ---
    tags:
      - Routes
    security:
      - BearerAuth: []
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: Route ID
    responses:
      200:
        description: Route deleted
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: Route deleted
      404:
        description: Route not found
      401:
        description: Unauthorized
    """
    route = Route.query.get(id)
    if not route:
        return jsonify({'success': False, 'message': 'Resource not found'}), 404
    
    db.session.delete(route)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Route deleted'
    })


@routes_bp.route('/search', methods=['GET'])
def search_routes():
    """
    Search Routes
    ---
    tags:
      - Routes
    parameters:
      - name: q
        in: query
        type: string
        required: true
        description: Search query (building name)
    responses:
      200:
        description: Search results
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            data:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    example: 5
                  start_building:
                    type: string
                    example: Main Gate
                  end_building:
                    type: string
                    example: Engineering Block
      400:
        description: Invalid input
    """
    query = request.args.get('q', '')
    if not query:
        return jsonify({'success': False, 'message': 'Invalid input'}), 400
    
    # Search routes where start or end building name matches
    routes = Route.query.join(
        Building, Route.start_building_id == Building.id
    ).filter(
        Building.name.ilike(f'%{query}%')
    ).all()
    
    # Also search by end building
    routes_by_end = Route.query.join(
        Building, Route.end_building_id == Building.id
    ).filter(
        Building.name.ilike(f'%{query}%')
    ).all()
    
    # Combine and deduplicate
    all_routes = {r.id: r for r in routes}
    for r in routes_by_end:
        all_routes[r.id] = r
    
    return jsonify({
        'success': True,
        'data': [
            {
                'id': r.id,
                'start_building': r.start_building.name if r.start_building else None,
                'end_building': r.end_building.name if r.end_building else None
            } for r in all_routes.values()
        ]
    })
