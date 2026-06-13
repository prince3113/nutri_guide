from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS
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
    CORS(app)

    migrate.init_app(app, db)   

    import os
    os.makedirs(os.path.join(app.root_path, 'static', 'uploads'), exist_ok=True)

    from app.routes.auth import auth_bp
    from app.routes.health import health_bp
    from app.routes.ai import ai_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(health_bp)
    app.register_blueprint(ai_bp)

    return app