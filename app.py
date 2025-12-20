from app import db, create_app
from app.models.lecturer import Lecturer
from app.models.department import Department
from app.models.building import Building
from flask import request, jsonify

app = create_app()

# Lecturers Routes
@app.route('/lecturers', methods=['GET'])
def lecturers():
    try:
        all_lects = Lecturer.query.all()
        lect_list = []
        for lect in all_lects:
            lect_list.append({
                "id":lect.id,
                "first_name":lect.first_name,
                "last_name":lect.last_name,
                "email":lect.email,
                "office_number":lect.office_number
            })
        return jsonify({
            "message": "Here is the list of all lecturers",
            "count": len(lect_list),
            "data": lect_list
        })
    except:
        db.session.rollback()
        return jsonify({"error": "Failed to fetch lecturers."}), 500

@app.route('/lecturers/<int:id>', methods = ["GET"])
def getlect(id):
    target = Lecturer.query.get_or_404(id)
    try:
        lect = {
            "id":target.id,
            "first_name":target.first_name,
            "last_name":target.last_name,
            "email":target.email,
            "office_number":target.office_number
        }
        return jsonify({
            "message": "Target Lecturer found",
            "data": lect
        })
    except:
        return jsonify({"error": "Error handling request"}), 500

@app.route('/lecturers', methods=["POST"])
def create_lecturer():
    data = request.get_json()
    if not data:
            return jsonify({"error": "No data provided"}), 400
    try:
        dept_id = data.get("department_id")
        building_id = data.get("office_building_id")
        
        # Check if Department exists
        if not db.session.get(Department, dept_id) :
            return jsonify({"error": "Invalid department_id"}), 400
            
        # Check if Building exists
        if not db.session.get(Building, building_id):
            return jsonify({"error": "Invalid office_building_id"}), 400
        
        # Creates new Lecturer instance
        new_lect = Lecturer(
            first_name = data.get("first_name"),
            last_name = data.get("last_name"),
            email=data.get("email"),
            department_id=data.get("department_id"),
            office_building_id=data.get("office_building_id"),
            office_number=data.get("office_number")
        )
        db.session.add(new_lect)
        db.session.commit()
        return jsonify({"message": f"Lecturer {new_lect.last_name} {new_lect.first_name} with email {new_lect.email} added successfully"}), 201
    except:
        db.session.rollback()
        return jsonify({"error": "issue creating new lecturer. check your names and email"}), 500

@app.route('/lecturers/<int:id>', methods = ["PUT", "DELETE"])
def handlelect(id):
    target = Lecturer.query.get_or_404(id)
    try:
        if request.method == "PUT":
            data = request.get_json()

            target.first_name = data.get("first_name", target.first_name)
            target.last_name = data.get("last_name", target.last_name)
            target.email = data.get("email", target.email)
            target.office_number = data.get("office_number", target.office_number)
            
            # Update Foreign Keys (Important!)
            if "department_id" in data:
                target.department_id = data.get("department_id")
            if "office_building_id" in data:
                target.office_building_id = data.get("office_building_id")

            db.session.commit()
            return jsonify({"message": "Lecturer updated successfully", "id": target.id})
        elif request.method == "DELETE":
            try:
                db.session.delete(target)
                db.session.commit()
                return jsonify({"message": f"lecturer of id {id} deleted"}), 200
            except Exception as e:
                print(f"DEBUG ERROR: {e}")
                db.session.rollback()
                return jsonify({"error": "Error deleting lecturer", "details": str(e)}), 500
    except Exception as e:
        print(f"DEBUG ERROR: {e}")
        db.session.rollback()
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500

        
if __name__ == "__main__":
    app.run(debug=True)
