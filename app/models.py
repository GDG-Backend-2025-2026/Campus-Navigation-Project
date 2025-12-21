from .extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash

class College(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    code = db.Column(db.String(10), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def create_demo_user(cls):
        """Create demo user if not exists"""
        if not cls.query.filter_by(username='osazuwa').first():
            user = cls(
                username='osazuwa',
                password=generate_password_hash('osazuwa1234')
            )
            db.session.add(user)
            db.session.commit()
            return user
