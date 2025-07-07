import os
from langchain_groq import ChatGroq
from langchain_community.chat_message_histories import FirestoreChatMessageHistory
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, Tool
from langchain_community.tools.google_serper import GoogleSerperRun
from firebase_admin import firestore
from config import GROQ_API_KEY
from tools.suggestion_engine import suggest_improvements

# Assurez-vous que votre clé API est valide et que Firestore est bien initialisé
# Initialiser le LLM Groq avec votre clé API et le modèle
llm = ChatGroq(api_key=GROQ_API_KEY, model="llama3-70b-8192")

def get_sylph_agent(user_id: str, session_id: str):
    """Retourne un agent Sylph prêt à interagir avec l'utilisateur."""
    
    # Connexion à Firestore et récupération de l'historique du chat
    firestore_client = firestore.client()  # Assurez-vous que Firebase est bien initialisé avant l'appel
    chat_history = FirestoreChatMessageHistory(
            collection_name="conversations",  # Nom de la collection dans Firestore
            session_id=session_id,             # UID de l'utilisateur comme session_id
            user_id=user_id,                # Utiliser l'UID comme user_id
            firestore_client=None            # Si tu as un client Firestore personnalisé, tu peux le passer ici
        )    
    # Initialisation de la mémoire avec l'historique des messages
    memory = ConversationBufferMemory(
        chat_memory=chat_history, 
        return_messages=True, 
        memory_key="chat_history"
    )
    
    # Nouvelle personnalité améliorée pour l'agent
    personality_prompt = (
        "Tu es Sylph, un assistant intelligent et professionnel. Evite de te présenter à chaque message. "
        "Réponds de manière concise et précise. Si quelqu'un prononce le mot 'Sylph', tu réponds en disant que tu es là pour aider. "
        "Tu poses des questions pour clarifier si une commande est incomplète, mais tu ne t'éternises jamais. "
        "Ton objectif est de guider l'utilisateur vers des solutions plus efficaces et modernes sans répéter constamment des phrases de présentation."
    )
    
    # Outils que l'agent peut utiliser
    tools = [
        Tool(
            name="suggestion_engine",
            func=suggest_improvements,
            description="Propose des améliorations ou alternatives plus modernes ou efficaces à la demande utilisateur"
        )
    ]
    
    # Initialiser l'agent avec la mémoire et les outils définis
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent="conversational-react-description",
        memory=memory,
        verbose=True,
        agent_kwargs={"prefix": personality_prompt}
    )
    
    return agent
