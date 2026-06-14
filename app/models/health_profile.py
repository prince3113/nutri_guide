from app import db
from datetime import datetime

class HealthProfile(db.Model):
    __tablename__ = "health_profiles"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False,
        unique=True
    )

    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    height = db.Column(db.Float, nullable=False)  # cm
    weight = db.Column(db.Float, nullable=False)  # kg
    activity_level = db.Column(db.String(50), nullable=False)
    goal = db.Column(db.String(50), nullable=False)
    diet_type = db.Column(db.String(20), nullable=False, default="vegetarian")

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def __init__(self, user_id: int, age: int, gender: str,
                 height: float, weight: float, activity_level: str,
                 goal: str, diet_type: str = "vegetarian", **kwargs):
        self.user_id = user_id
        self.age = age
        self.gender = gender
        self.height = height
        self.weight = weight
        self.activity_level = activity_level
        self.goal = goal
        self.diet_type = diet_type