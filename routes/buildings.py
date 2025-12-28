from flask import Blueprint, request, jsonify
from models.building import Building
from utils.db import db
from utils.auth import jwt_required
from utils.cloudinary import upload_image

buildings_bp = Blueprint('buildings', __name__)


@buildings_bp.route('', methods=['GET'])
def get_buildings():
    """
    Get All Buildings
    ---
    tags:
      - Buildings
    responses:
      200:
        description: List of all buildings
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
                    example: 1
                  name:
                    type: string
                    example: Engineering Block
                  image_url:
                    type: string
                    example: https://image.com/building.jpg
                  description:
                    type: string
                    example: Main engineering faculty
    """
    buildings = Building.query.all()
    return jsonify({
        'success': True,
        'data': [
            {
                'id': b.id,
                'name': b.name,
                'image_url': b.image_url,
                'description': b.description
            } for b in buildings
        ]
    })


@buildings_bp.route('/<int:id>', methods=['GET'])
def get_building(id):
    """
    Get Building Details
    ---
    tags:
      - Buildings
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: Building ID
    responses:
      200:
        description: Building details
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            data:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
                name:
                  type: string
                  example: Engineering Block
                image_url:
                  type: string
                  example: https://image.com/building.jpg
                description:
                  type: string
                  example: Main engineering faculty
      404:
        description: Building not found
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            message:
              type: string
              example: Resource not found
    """
    building = Building.query.get(id)
    if not building:
        return jsonify({'success': False, 'message': 'Resource not found'}), 404
    
    return jsonify({
        'success': True,
        'data': {
            'id': building.id,
            'name': building.name,
            'image_url': building.image_url,
            'description': building.description
        }
    })


@buildings_bp.route('', methods=['POST'])
@jwt_required
def create_building():
    """
    Create Building (Admin)
    ---
    tags:
      - Buildings
    security:
      - BearerAuth: []
    consumes:
      - multipart/form-data
    parameters:
      - name: name
        in: formData
        type: string
        required: true
        description: Building name
      - name: description
        in: formData
        type: string
        required: false
        description: Building description
      - name: image
        in: formData
        type: file
        required: false
        description: Building image
    responses:
      201:
        description: Building created
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            data:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
                name:
                  type: string
                  example: Engineering Block
      400:
        description: Invalid input
      401:
        description: Unauthorized
    """
    # Get form data
    name = request.form.get('name')
    description = request.form.get('description')
    
    if not name:
        return jsonify({'success': False, 'message': 'Invalid input'}), 400
    
    # Handle image upload
    image_url = None
    if 'image' in request.files:
        image_file = request.files['image']
        if image_file.filename:
            upload_result = upload_image(image_file, folder="campus-navigation/buildings")
            if upload_result['success']:
                image_url = upload_result['url']
            else:
                error_msg = upload_result.get('error', 'Unknown error')
                print(f"[ERROR] Image upload failed: {error_msg}")
                return jsonify({'success': False, 'message': 'Image upload failed', 'error': error_msg}), 400
    
    building = Building(
        name=name,
        description=description,
        image_url=image_url
    )
    db.session.add(building)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'data': {
            'id': building.id,
            'name': building.name
        }
    }), 201


@buildings_bp.route('/<int:id>', methods=['PUT'])
@jwt_required
def update_building(id):
    """
    Update Building (Admin)
    ---
    tags:
      - Buildings
    security:
      - BearerAuth: []
    consumes:
      - multipart/form-data
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: Building ID
      - name: name
        in: formData
        type: string
        required: false
        description: New building name
      - name: description
        in: formData
        type: string
        required: false
        description: New building description
      - name: image
        in: formData
        type: file
        required: false
        description: New building image
    responses:
      200:
        description: Building updated
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: Building updated
      404:
        description: Building not found
      401:
        description: Unauthorized
    """
    building = Building.query.get(id)
    if not building:
        return jsonify({'success': False, 'message': 'Resource not found'}), 404
    
    # Get form data
    name = request.form.get('name')
    description = request.form.get('description')
    
    if name:
        building.name = name
    if description is not None:
        building.description = description
    
    # Handle image upload
    if 'image' in request.files:
        image_file = request.files['image']
        if image_file.filename:
            upload_result = upload_image(image_file, folder="campus-navigation/buildings")
            if upload_result['success']:
                building.image_url = upload_result['url']
            else:
                error_msg = upload_result.get('error', 'Unknown error')
                print(f"[ERROR] Image upload failed: {error_msg}")
                return jsonify({'success': False, 'message': 'Image upload failed', 'error': error_msg}), 400
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Building updated'
    })


@buildings_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required
def delete_building(id):
    """
    Delete Building (Admin)
    ---
    tags:
      - Buildings
    security:
      - BearerAuth: []
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: Building ID
    responses:
      200:
        description: Building deleted
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: Building deleted
      404:
        description: Building not found
      401:
        description: Unauthorized
    """
    building = Building.query.get(id)
    if not building:
        return jsonify({'success': False, 'message': 'Resource not found'}), 404
    
    db.session.delete(building)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Building deleted'
    })


@buildings_bp.route('/search', methods=['GET'])
def search_buildings():
    """
    Search Buildings
    ---
    tags:
      - Buildings
    parameters:
      - name: q
        in: query
        type: string
        required: true
        description: Search query
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
                    example: 1
                  name:
                    type: string
                    example: Engineering Block
      400:
        description: Invalid input
    """
    query = request.args.get('q', '')
    if not query:
        return jsonify({'success': False, 'message': 'Invalid input'}), 400
    
    buildings = Building.query.filter(Building.name.ilike(f'%{query}%')).all()
    
    return jsonify({
        'success': True,
        'data': [
            {
                'id': b.id,
                'name': b.name
            } for b in buildings
        ]
    })
