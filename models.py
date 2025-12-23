from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class College(db.Model):
    __tablename__ = "colleges"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    # Relationship back to Department
    departments = db.relationship("Department", backref="college", lazy=True)

class Department(db.Model):
    __tablename__ = "departments"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(10), nullable=False)
    college_id = db.Column(db.Integer, db.ForeignKey("colleges.id"), nullable=False)
    
    # COMMENTED OUT UNTIL LECTURER MODEL IS ADDED
    # lecturers = db.relationship("Lecturer", backref="department", lazy=True)