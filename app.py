from app import db, create_app
from app.models.lecturer import Lecturer
from app.models.department import Department
from app.models.building import Building
from flask import request, jsonify

app = create_app()

# Handlers
def api_response(success, data=None, message="", errors=None, status=200):
    payload = {
        "success": success,
        "data": data,
        "message": message,
        "errors": errors,
        "meta": {
            "request_id": request.environ.get('FLASK_REQUEST_ID', 'N/A'),
            "timestamp": request.environ.get('FLASK_REQUEST_TIMESTAMP', 'N/A')
        }
    }
    return jsonify(payload), status

# Lecturers Routes
@app.route('/lecturers', methods=['GET'])
def lecturers():
    try:
        page_str = request.args.get('page', '1')
        per_page_str = request.args.get('per_page', '10')

        if not page_str.isdigit() or not per_page_str.isdigit():
            #Error Response
            return api_response(
                success=False,
                data=None,
                message=f"Page and per_page must be positive integers. received: page= {page_str}, per_page= {per_page_str}",
                errors="Invalid query parameters",
                status=400
            )

        page = int(page_str)
        per_page = int(per_page_str)

        pagination_obj = Lecturer.query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )

        if not pagination_obj.items and page > 1:
            #Error Response
            return api_response(
                success=False,
                data=None,
                message=f"You requested page {page}, but only {pagination_obj.pages} pages exist.",
                errors="Page not found",
                status=404
            )

        lect_list = []
        for lect in pagination_obj.items:
            lect_list.append({
                "id": lect.id,
                "first_name": lect.first_name,
                "last_name": lect.last_name,
                "email": lect.email,
                "office_number": lect.office_number,
                "department_id": lect.department_id,
                "office_building_id": lect.office_building_id
            })

        return jsonify({
            "success": True,
            "data": lect_list,
            "message": "Lecturers retrieved successfully",
            "errors": None,
            "meta": {
                "total_count": pagination_obj.total,
                "page": pagination_obj.page,
                "limit": pagination_obj.per_page,
                "total_pages": pagination_obj.pages,
            },
        }), 200
    
    except Exception as e:
        #Error Response
        db.session.rollback()
        return api_response(
            success=False,
            data=None,
            message="An error occurred fetching lecturers.",
            errors=str(e),
            status=500
        )

@app.route('/lecturers/<int:id>', methods = ["GET"])
def getlect(id):
    target = db.session.get(Lecturer, id)
    if not target:
        return api_response(
            success=False,
            data=None,
            message=f"Lecturer with id {id} does not exist.",
            errors={"id": "Resource not found"},
            status=404
        )
    
    try:
        lect = {
            "id":target.id,
            "first_name":target.first_name,
            "last_name":target.last_name,
            "email":target.email,
            "office_number":target.office_number,
            "department_id":target.department_id,
            "office_building_id":target.office_building_id
        }
        return api_response(
            success=True,
            data=lect,
            message="Target Lecturer found",
            errors=None,
            status=200
        )
    
    except Exception as e:
        #Error Response
        return api_response(
            success=False,
            data=None,
            message="An error occurred fetching lecturer.",
            errors=str(e),
            status=500
        )
        

@app.route('/lecturers', methods=["POST"])
def create_lecturer():
    if not request.is_json:
        #Error 
        return api_response(
            success=False,
            data=None,
            message="Please set Content-Type header to 'application/json'",
            errors="Invalid Media Type",
            status=415
        )

    data = request.get_json(silent=True)
    
    if data is None:
        #Error Response
        return api_response(
            success=False,
            data=None,
            message="The JSON body is empty or contains syntax errors (check your commas and quotes).",
            errors="Malformed JSON Request",
            status=400
        )

    required_fields = ["first_name", "last_name", "email", "department_id", "office_building_id"]
    missing = [f for f in required_fields if f not in data]
    if missing:
        #Error Response
        return api_response(
            success=False,
            data=None,
            message=f"The following fields are don't have valid data: {', '.join(missing)}",
            errors="Missing Data",
            status=400
        )
    
    expected_types = {
        "first_name": str,
        "last_name": str,
        "email": str,
        "department_id": int,
        "office_building_id": int,
        "office_number": str
    }

    type_errors = {}
    for field, expected_type in expected_types.items():
        if field in data and not isinstance(data[field], expected_type):
            type_errors[field] = f"Expected {expected_type.__name__}, got {type(data[field]).__name__}"

    if type_errors:
        # Error Response
        return api_response(
            success=False,
            data=None,
            message="Validation failed: Incorrect data types",
            errors=type_errors,
            status=400
        )

    existing_lecturer = Lecturer.query.filter_by(email=data.get("email")).first()
    if existing_lecturer:
        #Error Response
        return api_response(
            success=False,
            data=None,
            message=f"A lecturer with the email '{data.get('email')}' already exists.",
            errors="Data Conflict",
            status=409
        )
    
    # Validate Foreign Keys
    dept_id = data.get("department_id")
    building_id = data.get("office_building_id")
    
    # Check if Department exists
    if not db.session.get(Department, dept_id) :
        #Error Response
        return api_response(
            success=False,
            data=None,
            message=f"Invalid department_id: {dept_id} does not exist.",
            errors={
                "department_id": f"Department {dept_id} does not exist."
            },
            status=400
        )
        
    # Check if Building exists
    if not db.session.get(Building, building_id):
        #Error Response
        return api_response(
            success=False,
            data=None,
            message=f"Invalid office_building_id: {building_id} does not exist.",
            errors={
                "office_building_id": f"Building {building_id} does not exist."
            },
            status=400
        )
    
    try:
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
        return api_response(
            success=True,
            data={
                "id": new_lect.id,
                "first_name": new_lect.first_name,
                "last_name": new_lect.last_name,
                "email": new_lect.email,
                "office_number": new_lect.office_number,
                "department_id": new_lect.department_id,
                "office_building_id": new_lect.office_building_id
            },
            message="Lecturer data added successfully",
            errors=None,
            status=201
        )
    
    except Exception as e:
        #Error Response
        db.session.rollback()
        return api_response(
            success=False,
            data=None,
            message="Database error creating new lecturer.",
            errors=str(e),
            status=500
        )

@app.route('/lecturers/<int:id>', methods = ["PUT", "DELETE"])
def handle_lecturer(id):
    target = db.session.get(Lecturer, id)
    if not target:
        return api_response(
            success=False,
            data=None,
            message=f"Lecturer with id {id} does not exist.",
            errors={"id": "Resource not found"},
            status=404
        )
        
    try:
        if request.method == "PUT":
            data = request.get_json(silent=True)

            expected_types = {
                "first_name": str,
                "last_name": str,
                "email": str,
                "department_id": int,
                "office_building_id": int,
                "office_number": str
            }

            type_errors = {}
            for field in data:
                if field in expected_types and not isinstance(data[field], expected_types[field]):
                    type_errors[field] = f"Expected {expected_types[field].__name__}"

            if type_errors:
                return api_response(
                    success=False,
                    data=None,
                    message="Validation failed: Incorrect data types",
                    errors=type_errors,
                    status=400
                )
            
            # Update Foreign Keys (Important!)
            if "department_id" in data:
                # Check if Department exists
                if not db.session.get(Department, data.get("department_id")):
                    #Error Response
                    db.session.rollback()
                    return api_response(
                        success=False,
                        data=None,
                        message=f"Department of id {data.get('department_id')} does not exist.",
                        errors="Invalid department_id",
                        status=400
                    )
                target.department_id = data.get("department_id")
                
            
            if "office_building_id" in data:
                # Check if Building exists
                if not db.session.get(Building, data.get("office_building_id")):
                    #Error Response
                    db.session.rollback()
                    return api_response(
                        success=False,
                        data=None,
                        message=f"Building of id {data.get('office_building_id')} does not exist.",
                        errors="Invalid office_building_id",
                        status=400
                    )
                target.office_building_id = data.get("office_building_id")

            target.first_name = data.get("first_name", target.first_name)
            target.last_name = data.get("last_name", target.last_name)
            target.email = data.get("email", target.email)
            target.office_number = data.get("office_number", target.office_number)
            
            try:
                db.session.commit()
                return api_response(
                    success=True,
                    data={
                        "id": target.id,
                        "first_name": target.first_name,
                        "last_name": target.last_name,
                        "email": target.email,
                        "office_number": target.office_number,
                        "department_id": target.department_id,
                        "office_building_id": target.office_building_id
                    },
                    message="Lecturer updated successfully",
                    errors=None,
                    status=200
                )
                
            except Exception as e:
                #Error Response
                db.session.rollback()
                return api_response(
                    success=False,
                    data=None,
                    message="Database error updating lecturer.",
                    errors=str(e),
                    status=500
                )
        elif request.method == "DELETE":
            try:
                db.session.delete(target)
                db.session.commit()
                return "", 204
            except Exception as e:
                #Error Response
                print(f"DEBUG ERROR: {e}")
                db.session.rollback()
                return api_response(
                    success=False,
                    data=None,
                    message=f"Error deleting lecturer({type(e).__name__})",
                    errors=str(e),
                    status=500
                )
    except Exception as e:
        #Error Response
        print(f"DEBUG ERROR: {e}")
        db.session.rollback()
        return api_response(
            success=False,
            data=None,
            message=f"An unexpected error occurred({type(e).__name__})",
            errors=str(e),
            status=500
        )

if __name__ == "__main__":
    app.run(debug=True)
