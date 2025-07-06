from flask import Flask
import firebase_admin
from routes.chatbot import chatbot_bp
from config import FIREBASE_CREDENTIAL
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Initialisation Firebase depuis les credentials base64
firebase_admin.initialize_app(FIREBASE_CREDENTIAL)

# Flask app
app = Flask(__name__)
app.register_blueprint(chatbot_bp, url_prefix="/api")

# if __name__ == "__main__":
#     app.run(debug=True)
