from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_login import LoginManager
import os

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_secret_key')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///transport_app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt_secret_key')
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'qr_codes')

    CORS(app)
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'admin_login'

    from .models import User, Destination, Ticket
    from .routes.api_auth import api_auth_bp
    from .routes.api_user import api_user_bp
    from .routes.web_admin import web_admin_bp

    app.register_blueprint(api_auth_bp, url_prefix='/api/auth')
    app.register_blueprint(api_user_bp, url_prefix='/api/user')
    app.register_blueprint(web_admin_bp, url_prefix='/admin')

    # Créer le dossier QR code si nécessaire
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    return app
