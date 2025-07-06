def suggest_improvements(user_input: str) -> str:
    """
    Analyse le prompt utilisateur et propose une alternative ou amélioration.
    """
    lower_input = user_input.lower()

    if "flask" in lower_input and "fastapi" not in lower_input:
        return ("Flask est un bon choix. Mais FastAPI pourrait être une meilleure alternative : "
                "plus rapide, typé, et mieux pour les APIs modernes. Souhaites-tu que je le remplace ?")

    if "react native" in lower_input and "flutter" not in lower_input:
        return ("React Native est populaire. Mais Flutter pourrait être plus efficace pour un rendu natif unifié. "
                "Je peux te générer les deux bases si tu veux comparer.")

    return "Ta demande est cohérente. Je peux m’en occuper comme prévu, sauf si tu veux explorer d’autres options."

