from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import User, Destination, Ticket
from app.utils.qrcode_utils import generate_qr_code
from datetime import datetime
import os

# Blueprint pour les routes utilisateur (destinations, tickets, validation)
api_user_bp = Blueprint('api_user_bp', __name__)

@api_user_bp.route('/destinations', methods=['GET'])
@jwt_required()
def get_destinations():
    """
    Retourne la liste des destinations disponibles.
    Accessible uniquement avec un JWT valide.
    """
    destinations = Destination.query.all()
    return jsonify([{'id': d.id, 'depart': d.depart, 'arrivee': d.arrivee, 'compagnie': d.compagnie, 'prix': d.prix} for d in destinations])

@api_user_bp.route('/tickets', methods=['GET'])
@jwt_required()
def get_tickets():
    """
    Retourne la liste des tickets de l'utilisateur connecté.
    """
    user_id = get_jwt_identity()['id']
    tickets = Ticket.query.filter_by(user_id=user_id).all()
    return jsonify([
        {
            'id': t.id,
            'destination': {
                'depart': t.destination.depart,
                'arrivee': t.destination.arrivee,
                'compagnie': t.destination.compagnie,
                'prix': t.destination.prix
            },
            'date_voyage': t.date_voyage.strftime('%Y-%m-%d'),
            'status': t.status,
            'qr_code_path': t.qr_code_path
        } for t in tickets
    ])

@api_user_bp.route('/tickets', methods=['POST'])
@jwt_required()
def add_ticket():
    """
    Ajoute un ticket pour l'utilisateur connecté.
    Attend un JSON avec : destination_id, date_voyage (YYYY-MM-DD).
    """
    user_id = get_jwt_identity()['id']
    data = request.get_json()
    destination_id = data.get('destination_id')
    date_voyage = data.get('date_voyage')
    try:
        date_obj = datetime.strptime(date_voyage, '%Y-%m-%d').date()
    except Exception:
        return jsonify({'msg': 'Date invalide'}), 400
    ticket = Ticket(user_id=user_id, destination_id=destination_id, date_voyage=date_obj)
    db.session.add(ticket)
    db.session.commit()
    return jsonify({'msg': 'Ticket ajouté', 'ticket_id': ticket.id}), 201

@api_user_bp.route('/tickets/<int:ticket_id>/validate', methods=['POST'])
@jwt_required()
def validate_ticket(ticket_id):
    """
    Valide un ticket pour l'utilisateur connecté.
    """
    user_id = get_jwt_identity()['id']
    ticket = Ticket.query.filter_by(id=ticket_id, user_id=user_id).first()
    if not ticket:
        return jsonify({'msg': 'Ticket introuvable'}), 404
    if ticket.status == 'valide':
        return jsonify({'msg': 'Déjà validé'}), 400
    ticket.status = 'valide'
    qr_filename = generate_qr_code(ticket.id, current_app.config['UPLOAD_FOLDER'])
    ticket.qr_code_path = f'static/qr_codes/{qr_filename}'
    db.session.commit()
    return jsonify({'msg': 'Ticket validé', 'qr_code_path': ticket.qr_code_path}), 200
