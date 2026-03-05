from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config=None):
    app = Flask(__name__)

    app.config.setdefault("SQLALCHEMY_DATABASE_URI", "sqlite:///app.db")
    app.config.setdefault("SQLALCHEMY_TRACK_MODIFICATIONS", False)
    app.config.setdefault("SECRET_KEY", "dev-secret-key-change-in-production")

    if config:
        app.config.update(config)

    db.init_app(app)

    from app.routes.users import users_bp
    from app.routes.auth import auth_bp

    app.register_blueprint(users_bp, url_prefix="/users")
    app.register_blueprint(auth_bp, url_prefix="/auth")

    with app.app_context():
        db.create_all()

    return app
