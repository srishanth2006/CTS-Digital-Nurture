from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from extensions import db
from models.user import User
def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "super-secret-key"

    db.init_app(app)
    Migrate(app, db)
    JWTManager(app)

    from auth.routes import auth_bp
    app.register_blueprint(auth_bp)   # ✅ THIS MUST EXIST

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)