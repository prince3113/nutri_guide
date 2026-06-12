class config:
    SECRET_KEY = "mysecrestkey"
    SQLALCHEMY_DATABASE_URI = ("postgresql://postgres:root@localhost:5433/nutri_guide")
    SQLALCHEMY_TRACK_MODIFICATIONS = False