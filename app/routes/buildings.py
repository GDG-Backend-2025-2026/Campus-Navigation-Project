# routes/building.py
from flask import Blueprint, request, jsonify
from app.models.building import Building
from app import db
from sqlalchemy.exc import SQLAlchemyError

buildings_bp = Blueprint("buildings", __name__, url_prefix="/buildings")

# GET all buildings with pagination
@buildings_bp.route("/", methods=["GET"])
def get_all_buildings():
    # Get pagination parameters from query string with defaults
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    
    # Validate pagination parameters
    if page < 1:
        return jsonify({"error": "Page must be greater than 0"}), 400
    if per_page < 1 or per_page > 100:  # Limit max items per page
        return jsonify({"error": "per_page must be between 1 and 100"}), 400
    
    #  paginate() used instead of all() for efficient querying
    pagination = Building.query.paginate(page=page, per_page=per_page, error_out=False)
    
    # Build response with pagination metadata
    data = {
        "page": pagination.page,
        "per_page": pagination.per_page,
        "total_pages": pagination.pages,
        "total_items": pagination.total,
        "has_next": pagination.has_next,
        "has_prev": pagination.has_prev,
        "items": [{"id": b.id, "name": b.name, "description": b.description, "image_url": b.image_url} 
                 for b in pagination.items]
    }
    return jsonify(data), 200

# GET single building by ID
@buildings_bp.route("/<int:building_id>", methods=["GET"])
def get_building(building_id):
    building = Building.query.get(building_id)
    if not building:
        return jsonify({"error": "Building not found"}), 404
    return jsonify({
        "id": building.id,
        "name": building.name,
        "description": building.description,
        "image_url": building.image_url
    }), 200

# CREATE a new building
@buildings_bp.route("/", methods=["POST"])
def create_building():
    data = request.get_json()
    
    # Input validation 
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400
    
    # Extract and validate required fields
    name = data.get("name")
    description = data.get("description")
    image_url = data.get("image_url")
    
    # Validate name (required)
    if not name:
        return jsonify({"error": "Building name is required"}), 400
    
    # Additional validation rules
    if not isinstance(name, str) or len(name.strip()) == 0:
        return jsonify({"error": "Name must be a non-empty string"}), 400
    
    if len(name.strip()) > 100:  # length constraint
        return jsonify({"error": "Name cannot exceed 100 characters"}), 400
    
    # field validations
    if description and (not isinstance(description, str) or len(description) > 500):
        return jsonify({"error": "Description must be a string under 500 characters"}), 400
    
    if image_url and (not isinstance(image_url, str) or len(image_url) > 255):
        return jsonify({"error": "Image URL must be a string under 255 characters"}), 400
    
    # Database operation with error handling
    try:
        new_building = Building(
            name=name.strip(),   # type: ignore
            description=description.strip() if description else None,  # type: ignore
            image_url=image_url.strip() if image_url else None   # type: ignore
        ) # type: ignore
        db.session.add(new_building)
        db.session.commit()
        
        return jsonify({
            "message": "Building created successfully",
            "id": new_building.id,
            "building": {
                "id": new_building.id,
                "name": new_building.name,
                "description": new_building.description,
                "image_url": new_building.image_url
            }
        }), 201
        
    except SQLAlchemyError as e:
        db.session.rollback()  # Critical: rollback on failure
        # Log the actual error for debugging (in production, use logging module)
        # logging.error(f"Database error in create_building: {str(e)}")
        return jsonify({"error": "Database error occurred while creating building"}), 500

# UPDATE building by ID
@buildings_bp.route("/<int:building_id>", methods=["PUT"])
def update_building(building_id):
    # Check if building exists first
    building = Building.query.get(building_id)
    if not building:
        return jsonify({"error": "Building not found"}), 404
    
    data = request.get_json()
    
    # Input validation for UPDATE
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400
    
    # Extract fields
    name = data.get("name")
    description = data.get("description")
    image_url = data.get("image_url")
    
    # Validate provided fields (all optional for UPDATE but must be valid if provided)
    if "name" in data:
        if not name or not isinstance(name, str) or len(name.strip()) == 0:
            return jsonify({"error": "Name must be a non-empty string"}), 400
        if len(name.strip()) > 100:
            return jsonify({"error": "Name cannot exceed 100 characters"}), 400
        building.name = name.strip()
    
    if "description" in data:
        if description is not None:  # Allow null/empty description
            if not isinstance(description, str):
                return jsonify({"error": "Description must be a string"}), 400
            if len(description) > 500:
                return jsonify({"error": "Description cannot exceed 500 characters"}), 400
            building.description = description.strip() if description.strip() else None
    
    if "image_url" in data:
        if image_url is not None:  # Allow null/empty image_url
            if not isinstance(image_url, str):
                return jsonify({"error": "Image URL must be a string"}), 400
            if len(image_url) > 255:
                return jsonify({"error": "Image URL cannot exceed 255 characters"}), 400
            building.image_url = image_url.strip() if image_url.strip() else None
    
    # Database operation with error handling
    try:
        db.session.commit()
        return jsonify({
            "message": "Building updated successfully",
            "building": {
                "id": building.id,
                "name": building.name,
                "description": building.description,
                "image_url": building.image_url
            }
        }), 200
        
    except SQLAlchemyError as e:
        db.session.rollback()  # Critical: rollback on failure
        # logging.error(f"Database error in update_building: {str(e)}")
        return jsonify({"error": "Database error occurred while updating building"}), 500

# DELETE building by ID
@buildings_bp.route("/<int:building_id>", methods=["DELETE"])
def delete_building(building_id):
    building = Building.query.get(building_id)
    if not building:
        return jsonify({"error": "Building not found"}), 404
    
    # Database operation with error handling
    try:
        db.session.delete(building)
        db.session.commit()
        return jsonify({"message": "Building deleted successfully"}), 200
        
    except SQLAlchemyError as e:
        db.session.rollback()  # Critical: rollback on failure
        # logging.error(f"Database error in delete_building: {str(e)}")
        return jsonify({"error": "Database error occurred while deleting building"}), 500