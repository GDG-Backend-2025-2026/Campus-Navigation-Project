# routes/building.py
from tkinter.font import names
from flask import Blueprint, request, jsonify
from app.models.building import Building
from app import db

buildings_bp = Blueprint("buildings", __name__, url_prefix="/buildings")

# GET all buildings (no auth)
@buildings_bp.route("/", methods=["GET"])
def get_all_buildings():
    buildings = Building.query.all()
    data = [{"id": b.id, "name": b.name, "description": b.description, "image_url": b.image_url} for b in buildings]
    return jsonify(data), 200

# GET single building by ID (no auth)
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

# CREATE a new building (no auth for now)
@buildings_bp.route("/", methods=["POST"])
def create_building():
    data = request.get_json()
    name = data.get("name")
    description = data.get("description")
    image_url = data.get("image_url")

    if not name:
        return jsonify({"error": "Building name is required"}), 400

    new_building = Building(name=name, description=description, image_url=image_url) #type: ignore
    db.session.add(new_building)
    db.session.commit()
    return jsonify({"message": "Building created", "id": new_building.id}), 201

# UPDATE building by ID (no auth for now)
@buildings_bp.route("/<int:building_id>", methods=["PUT"])
def update_building(building_id):
    building = Building.query.get(building_id)
    if not building:
        return jsonify({"error": "Building not found"}), 404

    data = request.get_json()
    name = data.get("name")
    description = data.get("description")
    image_url = data.get("image_url")

    if name:
        building.name = name
    if description:
        building.description = description
    if image_url:
        building.image_url = image_url

    db.session.commit()
    return jsonify({"message": "Building updated"}), 200

# DELETE building by ID (no auth for now)
@buildings_bp.route("/<int:building_id>", methods=["DELETE"])
def delete_building(building_id):
    building = Building.query.get(building_id)
    if not building:
        return jsonify({"error": "Building not found"}), 404

    db.session.delete(building)
    db.session.commit()
    return jsonify({"message": "Building deleted"}), 200
