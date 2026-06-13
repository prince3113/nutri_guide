from app import db
from datetime import datetime, date


class WaterLog(db.Model):
    __tablename__ = "water_logs"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )

    log_date = db.Column(db.Date, nullable=False, default=date.today)
    glasses_consumed = db.Column(db.Integer, default=0)
    target_glasses = db.Column(db.Integer, default=8)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # Unique constraint: one log per user per day
    __table_args__ = (
        db.UniqueConstraint('user_id', 'log_date', name='uq_user_date'),
    )

    def __init__(self, user_id, target_glasses=8, **kwargs):
        self.user_id = user_id
        self.log_date = date.today()
        self.glasses_consumed = 0
        self.target_glasses = target_glasses
