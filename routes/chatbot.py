from flask import Blueprint, request, jsonify
from services.sylph_chatbot import get_sylph_agent

chatbot_bp = Blueprint('chatbot', __name__)

@chatbot_bp.route("/chat", methods=["POST"])
def sylph_chat():
    print("Requête reçue:", request.json)
    data = request.get_json()
    user_id = data.get("user_id")
    message = data.get("message")
    if not message or not user_id:
        return jsonify({"error": "user_id et message requis."}), 400

    agent = get_sylph_agent(user_id)
    response = agent.run(message)
    return jsonify({"response": response})
