import os
from app import create_app

#initialisation de l'application
app = create_app()

#page d'accueil
@app.route('/')
def index():
    return "<h1>Man debrouille toi !</h1>"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # 🔥 important pour Render
    app.run(host="0.0.0.0", port=port)
