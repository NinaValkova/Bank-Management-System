from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import os

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile("config.py", silent=True)

    app.config.from_mapping(
        SMTP_HOST=os.getenv("SMTP_HOST"),
        SMTP_PORT=int(os.getenv("SMTP_PORT", "587")),
        SMTP_USER=os.getenv("SMTP_USER"),
        SMTP_PASSWORD=os.getenv("SMTP_PASSWORD"),
        SUPPORT_EMAIL=os.getenv("SUPPORT_EMAIL"),
    )

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from .models import (
        account,
        admin,
        disposition,
        transaction,
        user,
        token_blocklist,
    )

    CORS(
        app,
        resources={
            r"/api/.*": {"origins": ["http://localhost:3000", "http://127.0.0.1:3000"]}
        },
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        supports_credentials=True,
    )

    from .user.api.routes import user_bp
    from .admin.api.routes import admin_bp

    app.register_blueprint(user_bp, url_prefix="/api/user")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")

    return app


#app = create_app()
