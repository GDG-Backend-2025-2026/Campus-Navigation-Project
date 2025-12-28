from utils.db import db


class Building(db.Model):
    __tablename__ = "buildings"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(255), nullable=True)

    # Relationships
    routes_from = db.relationship(
        "Route",
        foreign_keys="Route.start_building_id",
        backref="start_building",
        lazy=True
    )
    routes_to = db.relationship(
        "Route",
        foreign_keys="Route.end_building_id",
        backref="end_building",
        lazy=True
    )
