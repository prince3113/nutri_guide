from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from config import config


db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
migrate = Migrate()   

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    migrate.init_app(app, db)   

    from app.routes.auth import auth_bp
    from app.routes.health import health_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(health_bp)

    return app