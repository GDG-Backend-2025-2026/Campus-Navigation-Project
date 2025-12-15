from app import db

class Building(db.Model):
    __tablename__ = "buildings"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(255))

    # Relationships
    lecturers = db.relationship("Lecturer", backref="office_building", lazy=True)
    routes_from = db.relationship(
        "Route",
        foreign_keys="Route.origin_building_id",
        backref="origin_building",
        lazy=True
    )
    routes_to = db.relationship(
        "Route",
        foreign_keys="Route.destination_building_id",
        backref="destination_building",
        lazy=True
    )
