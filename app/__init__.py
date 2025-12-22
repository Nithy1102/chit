from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.secret_key = "rajesh-opticals-secret"

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    CORS(app, supports_credentials=True)
    db.init_app(app)

    from app.models.user import User
    from app.models.patient import Patient
    from .routes.auth import auth_bp
    from .routes.pages import pages_bp
    from app.routes.patients import patient_bp
    from app.routes.activity import activity_bp
    from app.routes.messages import messages_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(pages_bp)
    app.register_blueprint(patient_bp)
    app.register_blueprint(activity_bp)
    app.register_blueprint(messages_bp)

    with app.app_context():
     db.create_all()

    return app
