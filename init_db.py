from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    db.create_all()
    # Création d'un admin par défaut si inexistant
    if not User.query.filter_by(email='admin@transport.com').first():
        admin = User(nom='Admin', email='admin@transport.com', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print('Admin créé : admin@transport.com / admin123')
    else:
        print('Admin déjà existant.')
print('Base de données initialisée.')
