from flask import Blueprint, request, jsonify
from app import db, bcrypt
from app.models import User
from flask_jwt_extended import create_access_token

api_auth_bp = Blueprint('api_auth_bp', __name__)

@api_auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    nom = data.get('nom')
    email = data.get('email')
    password = data.get('password')
    if not all([nom, email, password]):
        return jsonify({'msg': 'Champs manquants'}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({'msg': 'Email déjà utilisé'}), 409
    user = User(nom=nom, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'msg': 'Inscription réussie'}), 201

@api_auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity={'id': user.id, 'role': user.role})
        return jsonify({'access_token': access_token, 'role': user.role}), 200
    return jsonify({'msg': 'Identifiants invalides'}), 401
