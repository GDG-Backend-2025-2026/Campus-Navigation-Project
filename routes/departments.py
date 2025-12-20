from flask import Blueprint, request, jsonify
from models import db, Department, College 

dept_bp = Blueprint('dept_bp', __name__)

# 1. GET ALL (No Auth)
@dept_bp.route('/departments', methods=['GET'])
def get_all():
    depts = Department.query.all()
    output = [{"id": d.id, "name": d.name, "code": d.code, "college_id": d.college_id} for d in depts]
    return jsonify(output), 200

# 2. GET SINGLE (No Auth)
@dept_bp.route('/departments/<int:id>', methods=['GET'])
def get_one(id):
    dept = Department.query.get_or_404(id)
    return jsonify({"id": dept.id, "name": dept.name, "code": dept.code, "college_id": dept.college_id}), 200

# 3. CREATE (Strengthened Validation)
@dept_bp.route('/departments', methods=['POST'])
def create():
    data = request.get_json()
    name = data.get('name')
    code = data.get('code')
    college_id = data.get('college_id')

    # 1. Validation for payload presence
    if not name or not code or not college_id:
        return jsonify({"error": "Name, Code, and College ID are required"}), 400

    # 2. Check if name or code already exists (Prevent duplicates)
    if Department.query.filter((Department.name == name) | (Department.code == code)).first():
        return jsonify({"error": "Department name or code already exists"}), 400

    # 3. Validate college_id exists
    college = College.query.get(college_id)
    if not college:
        return jsonify({"error": "The college_id provided does not exist"}), 400
    
    new_dept = Department(name=name, code=code, college_id=college_id)
    db.session.add(new_dept)
    db.session.commit()

    # RETURN the created department object
    return jsonify({
        "id": new_dept.id,
        "name": new_dept.name,
        "code": new_dept.code,
        "college_id": new_dept.college_id
    }), 201

# 4. UPDATE (Strengthened Validation)
@dept_bp.route('/departments/<int:id>', methods=['PUT'])
def update(id):
    dept = Department.query.get_or_404(id)
    data = request.get_json()
    
    # 1. Validate name and code aren't being updated to empty values
    if 'name' in data and not data['name']:
        return jsonify({"error": "Name cannot be empty"}), 400
    if 'code' in data and not data['code']:
        return jsonify({"error": "Code cannot be empty"}), 400

    # 2. Check if the new name or code is already taken by another department
    if 'name' in data:
        existing = Department.query.filter(Department.name == data['name'], Department.id != id).first()
        if existing:
            return jsonify({"error": "Another department already has this name"}), 400
        dept.name = data['name']

    if 'code' in data:
        existing = Department.query.filter(Department.code == data['code'], Department.id != id).first()
        if existing:
            return jsonify({"error": "Another department already has this code"}), 400
        dept.code = data['code']

    # 3. Validate college_id if it's being updated
    if 'college_id' in data:
        if not College.query.get(data['college_id']):
            return jsonify({"error": "Invalid college_id"}), 400
        dept.college_id = data['college_id']

    db.session.commit()

    # RETURN the updated department object
    return jsonify({
        "id": dept.id,
        "name": dept.name,
        "code": dept.code,
        "college_id": dept.college_id
    }), 200

# 5. DELETE
@dept_bp.route('/departments/<int:id>', methods=['DELETE'])
def delete(id):
    dept = Department.query.get_or_404(id)
    db.session.delete(dept)
    db.session.commit()
    return jsonify({"message": "Deleted"}), 200