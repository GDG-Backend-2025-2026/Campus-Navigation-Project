from app import db

class Route(db.Model):
    __tablename__ = "routes"

    id = db.Column(db.Integer, primary_key=True)
    origin_building_id = db.Column(db.Integer, db.ForeignKey("buildings.id"), nullable=False)
    destination_building_id = db.Column(db.Integer, db.ForeignKey("buildings.id"), nullable=False)

    # Relationships
    route_cards = db.relationship("RouteCard", backref="route", lazy=True)
