import os
import base64
import json
from dotenv import load_dotenv
from firebase_admin import credentials

load_dotenv()

# Clés API
encoded_key = os.getenv("GROQ_API_KEY")
GROQ_API_KEY = base64.b64decode(encoded_key).decode()

# Firebase credentials depuis base64
firebase_cred_b64 = os.getenv("FIREBASE_CREDENTIAL")
firebase_cred_json = json.loads(base64.b64decode(firebase_cred_b64))
FIREBASE_CREDENTIAL = credentials.Certificate(firebase_cred_json)
