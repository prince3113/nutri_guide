from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, name: str, email: str, password: str, **kwargs):
        self.name = name
        self.email = email
        self.password = password

    health_profiles = db.relationship(
    'HealthProfile',
    backref='user',
    lazy=True
)