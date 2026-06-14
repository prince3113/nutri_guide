from app import db
from datetime import datetime

class DietPlan(db.Model):
    __tablename__ = "diet_plans"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    daily_calories = db.Column(db.Integer)
    protein = db.Column(db.Float)
    carbs = db.Column(db.Float)
    fats = db.Column(db.Float)

    meal_plan = db.Column(db.JSON)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, user_id: int, daily_calories: int = None, protein: float = None,
                 carbs: float = None, fats: float = None, meal_plan=None, **kwargs):
        self.user_id = user_id
        self.daily_calories = daily_calories
        self.protein = protein
        self.carbs = carbs
        self.fats = fats
        self.meal_plan = meal_plan