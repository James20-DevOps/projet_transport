from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User, Destination, Ticket
from app import db, login_manager, bcrypt
from datetime import datetime
import os

web_admin_bp = Blueprint('web_admin_bp', __name__, template_folder='../templates/admin')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@web_admin_bp.route('/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email, role='admin').first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('web_admin_bp.dashboard'))
        flash('Identifiants invalides ou non admin', 'danger')
    return render_template('login.html')

@web_admin_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'admin':
        return redirect(url_for('web_admin_bp.admin_login'))
    return render_template('dashboard.html')

@web_admin_bp.route('/users')
@login_required
def users():
    if current_user.role != 'admin':
        return redirect(url_for('web_admin_bp.admin_login'))
    users = User.query.all()
    return render_template('users.html', users=users)

@web_admin_bp.route('/destinations', methods=['GET', 'POST'])
@login_required
def destinations():
    if current_user.role != 'admin':
        return redirect(url_for('web_admin_bp.admin_login'))
    if request.method == 'POST':
        depart = request.form['depart']
        arrivee = request.form['arrivee']
        compagnie = request.form['compagnie']
        prix = request.form['prix']
        d = Destination(depart=depart, arrivee=arrivee, compagnie=compagnie, prix=prix)
        db.session.add(d)
        db.session.commit()
        flash('Destination ajoutée', 'success')
    destinations = Destination.query.all()
    return render_template('destinations.html', destinations=destinations)

@web_admin_bp.route('/scan', methods=['GET', 'POST'])
@login_required
def scan():
    if current_user.role != 'admin':
        return redirect(url_for('web_admin_bp.admin_login'))
    result = None
    if request.method == 'POST':
        ticket_id = request.form.get('ticket_id')
        if ticket_id:
            ticket = Ticket.query.filter_by(id=ticket_id).first()
            if ticket:
                if ticket.status == 'valide' and not ticket.used:
                    ticket.status = 'utilisé'
                    ticket.used = True
                    db.session.commit()
                    result = f'Ticket {ticket.id} validé et marqué comme utilisé.'
                elif ticket.used:
                    result = 'Ce ticket a déjà été utilisé.'
                else:
                    result = 'Ce ticket n\'est pas valide.'
            else:
                result = 'Ticket introuvable.'
    return render_template('scan.html', result=result)

@web_admin_bp.route('/logout')
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('web_admin_bp.admin_login'))
