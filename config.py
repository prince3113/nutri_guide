import os

class config:
    SECRET_KEY = os.getenv("SECRET_KEY", "mysecrestkey")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://postgres:root@localhost:5433/nutri_guide")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")