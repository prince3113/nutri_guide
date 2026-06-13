from app import db
from datetime import datetime

class BMIRecord(db.Model):
    __tablename__ = "bmi_records"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    bmi = db.Column(db.Float)
    category = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)