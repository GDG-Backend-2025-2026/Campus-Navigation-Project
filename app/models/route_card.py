from app import db

class RouteCard(db.Model):
    __tablename__ = "route_cards"

    id = db.Column(db.Integer, primary_key=True)
    step_number = db.Column(db.Integer, nullable=False)
    instruction = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255))
    route_id = db.Column(db.Integer, db.ForeignKey("routes.id"), nullable=False)
