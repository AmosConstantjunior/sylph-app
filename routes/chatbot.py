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
    conversations_ref = db.collection("conversations").where("user_id", "==", user_id)
    docs = conversations_ref.stream()

    sessions = []
    seen_ids = set()

    for doc in docs:
        data = doc.to_dict()

        session_id = data.get("id")  # ou doc.id si tu veux
        if not session_id or session_id in seen_ids:
            continue
        seen_ids.add(session_id)

        # 🧠 Tenter de trouver le premier message humain pour nommer la session
        name = "Session"
        for msg in data.get("messages", []):
            if msg.get("type") == "human":
                name = msg["data"].get("content", "Session")
                break

        sessions.append({
            "id": session_id,
            "name": name[:50]  # tronque si c'est trop long
        })

    return jsonify({"sessions": sessions})

@chatbot_bp.route("/select_session/<session_id>/messages", methods=["GET"])
def get_messages_for_session(session_id):
    db = firestore.client()
    
    # Recherche la session dans Firestore avec son ID
    session_ref = db.collection("conversations").document(session_id)
    session = session_ref.get()
    
    if not session.exists:
        return jsonify({"error": "Session non trouvée."}), 404
    
    data = session.to_dict()
    messages = data.get("messages", [])
    
    # Renvoyer les messages de la session
    return jsonify({"messages": messages})
