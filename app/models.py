from . import db, bcrypt
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(10), default='user')
    tickets = db.relationship('Ticket', backref='user', lazy=True)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

class Destination(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    depart = db.Column(db.String(100), nullable=False)
    arrivee = db.Column(db.String(100), nullable=False)
    compagnie = db.Column(db.String(100), nullable=False)
    prix = db.Column(db.Float, nullable=False)
    tickets = db.relationship('Ticket', backref='destination', lazy=True)

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    destination_id = db.Column(db.Integer, db.ForeignKey('destination.id'), nullable=False)
    date_voyage = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='invalide')
    qr_code_path = db.Column(db.String(200), nullable=True)
    used = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
