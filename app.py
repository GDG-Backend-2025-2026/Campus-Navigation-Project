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
                "email":lect.email
            })
        return jsonify({
            "message": "Here is the list of all lecturers",
            "count": len(lect_list),
            "data": lect_list
        })
    except:
        return "Failed to fetch lecturers.", 500

@app.route('/lecturers/<int:id>', methods = ["GET"])
def getlect(id):
    try:
        target = Lecturer.query.get_or_404(id)
        if request.method == "GET":
            try:
                lect = {
                    "id":target.id,
                    "first_name":target.first_name,
                    "last_name":target.last_name,
                    "email":target.email
                }
                return jsonify({
                    "message": "Target Lecturer found",
                    "data": lect
                })
            except:
                return "Error fetching target", 500
       
    except:
        return "Error handling request", 500

        
if __name__ == "__main__":
    app.run(debug=True)
