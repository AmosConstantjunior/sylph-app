from flask import Blueprint, request, jsonify
from services.sylph_chatbot import get_sylph_agent
from firebase_admin import firestore


chatbot_bp = Blueprint('chatbot', __name__)

@chatbot_bp.route("/chat", methods=["POST"])
def sylph_chat():
    print("Requête reçue:", request.json)
    data = request.get_json()
    user_id = data.get("user_id")
    message = data.get("message")
    session_id = data.get("session_id")  # Nouvelle ligne

    if not message or not user_id:
        return jsonify({"error": "user_id et message requis."}), 400

    agent = get_sylph_agent(user_id, session_id=session_id)  # Utiliser user_id comme session_id
    response = agent.run(message)
    return jsonify({"response": response})


@chatbot_bp.route("/sessions", methods=["GET"])
def get_sessions():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id requis."}), 400

    db = firestore.client()
    
    # Suppose chaque document a un champ user_id et un champ session_id ou name
    conversations_ref = db.collection("conversations").where("user_id", "==", user_id)
    docs = conversations_ref.stream()
    
    session_ids = set()
    for doc in docs:
        data = doc.to_dict()
        session_id = data.get("session_id")  # Ou autre champ d'identifiant
        if session_id:
            session_ids.add(session_id)

    return jsonify({"sessions": list(session_ids)})


@chatbot_bp.route("/select_session", methods=["POST"])
def select_session():
    data = request.get_json()
    user_id = data.get("user_id")
    session_id = data.get("session_id")

    if not user_id or not session_id:
        return jsonify({"error": "user_id et session_id requis."}), 400

    agent = get_sylph_agent(user_id)
    agent.set_session(session_id)
    return jsonify({"message": f"Session {session_id} sélectionnée."})
