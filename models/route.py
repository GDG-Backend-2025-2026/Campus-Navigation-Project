from utils.db import db


class Route(db.Model):
    __tablename__ = "routes"

    id = db.Column(db.Integer, primary_key=True)
    start_building_id = db.Column(db.Integer, db.ForeignKey("buildings.id"), nullable=False)
    end_building_id = db.Column(db.Integer, db.ForeignKey("buildings.id"), nullable=False)

    # Relationships
    steps = db.relationship("RouteCard", backref="route", lazy=True, cascade="all, delete-orphan")

