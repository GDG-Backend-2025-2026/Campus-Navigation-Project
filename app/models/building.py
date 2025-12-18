from app import db

class Building(db.Model):
    __tablename__ = "buildings"

    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(100), nullable=False)
    description: str | None = db.Column(db.String(200))
    image_url: str | None = db.Column(db.String(255))

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
