import os
from flask import render_template  # Ajout pour le rendu de template
from app import create_app

# Initialisation de l'application Flask via la factory
app = create_app()

# Page d'accueil : Affiche la liste dynamique des routes de l'API et du site
@app.route('/')
def index():
    """
    Page d'accueil : affiche dynamiquement toutes les routes de l'application (API et web) dans un tableau HTML.
    Utile pour permettre à un collaborateur de voir tous les endpoints disponibles.
    """
    routes = []
    for rule in app.url_map.iter_rules():
        # On ignore les routes statiques Flask
        if rule.endpoint != 'static':
            routes.append({
                'endpoint': rule.endpoint,
                'methods': ', '.join(sorted(rule.methods - {'HEAD', 'OPTIONS'})),
                'rule': str(rule)
            })
    # Tri par URL pour plus de lisibilité
    routes = sorted(routes, key=lambda r: r['rule'])
    return render_template('index.html', routes=routes)

# Point d'entrée de l'application
if __name__ == "__main__":
    # Permet de lancer sur le port défini par Render ou par défaut sur 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
