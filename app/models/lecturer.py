from app import db

class Lecturer(db.Model):
    __tablename__ = "lecturers"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"), nullable=False)
    office_building_id = db.Column(db.Integer, db.ForeignKey("buildings.id"))
    office_number = db.Column(db.String(20))
