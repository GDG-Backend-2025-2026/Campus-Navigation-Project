from flask import Blueprint, request, jsonify
from models import db, Department, College # Import db from models, not app

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

# 3. CREATE (Validates college_id)
@dept_bp.route('/departments', methods=['POST'])
def create():
    data = request.get_json()
    # Task Requirement: Validate that college_id exists
    college = College.query.get(data.get('college_id'))
    if not college:
        return jsonify({"error": "The college_id provided does not exist"}), 400
    
    new_dept = Department(name=data['name'], code=data['code'], college_id=data['college_id'])
    db.session.add(new_dept)
    db.session.commit()
    return jsonify({"message": "Department created"}), 201

# 4. UPDATE (Validates college_id)
@dept_bp.route('/departments/<int:id>', methods=['PUT'])
def update(id):
    dept = Department.query.get_or_404(id)
    data = request.get_json()
    
    if 'college_id' in data:
        if not College.query.get(data['college_id']):
            return jsonify({"error": "Invalid college_id"}), 400
        dept.college_id = data['college_id']

    dept.name = data.get('name', dept.name)
    dept.code = data.get('code', dept.code)
    db.session.commit()
    return jsonify({"message": "Updated"}), 200

# 5. DELETE
@dept_bp.route('/departments/<int:id>', methods=['DELETE'])
def delete(id):
    dept = Department.query.get_or_404(id)
    db.session.delete(dept)
    db.session.commit()
    return jsonify({"message": "Deleted"}), 200