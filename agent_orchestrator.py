import os
import requests
from google import genai
from google.genai import types

client = genai.Client()

def call_agent(role_instruction, prompt_input):
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt_input,
        config=types.GenerateContentConfig(
            system_instruction=role_instruction,
            temperature=0.85,
        ),
    )
    return response.text

def send_telegram_message(message):
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    
    if not bot_token or not chat_id:
        print(message)
        return

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    max_length = 4000
    for i in range(0, len(message), max_length):
        chunk = message[i:i+max_length]
        payload = {"chat_id": chat_id, "text": chunk, "parse_mode": "Markdown"}
        requests.post(url, json=payload)

def daily_autonomous_mission():
    print("--- [MISSION 0 DH] Démarrage des agents (Zéro Budget) ---")
    
    # 1. Explorateur de Problèmes (Axé sur le gratuit et le récurrent)
    explorer_prompt = (
        "Tu es un expert en veille et opportunités digitales à ZERO BUDGET. "
        "Identifie UN problème urgent et actuel sur internet où les gens galèrent, "
        "mais pour lequel ils recherchent des astuces ou des outils gratuits."
    )
    problem = call_agent(explorer_prompt, "Trouve un pain-point brûlant du moment sur le web.")
    
    # 2. Agent Critique (Chasse aux coûts cachés)
    critic_prompt = (
        "Tu es l'agent critique intraitable sur le budget. "
        "Vérifie le problème trouvé : si la solution demande le moindre centime d'investissement (pub, hébergement payant, outil pro), "
        "détruis l'idée. On ne veut que du 0 dirham."
    )
    criticism = call_agent(critic_prompt, f"Problème :\n{problem}\nAnalyse les risques de coûts cachés.")

    # 3. Concepteur de Solution (100% Gratuit / Open Source / No-Code gratuit)
    solution_prompt = (
        "Conçois une solution qui coûte exactement 0 dirham à créer et déployer "
        "(ex: script Python gratuit sur GitHub, template partagé via Google Sheets/Notion gratuit, "
        "site hébergé gratuitement sur Netlify/GitHub Pages, ou contenu organique sur les réseaux)."
    )
    solution = call_agent(solution_prompt, f"Problème :\n{problem}\nPropose la solution technique 100% gratuite.")

    # 4. Stratège en Monétisation Organique (Cash immédiat sans pub)
    monetization_prompt = (
        "Comment monétiser cette solution gratuitement ? "
        "Exemples : liens d'affiliation (Amazon, 0 DH), dons (Ko-fi/Buy Me a Coffee), "
        "ou vente de services de mise en place directe via démarchage organique sur les réseaux sociaux. "
        "Donne le plan d'action d'acquisition 100% organique (sans un seul centime de pub)."
    )
    monetization = call_agent(monetization_prompt, f"Solution :\n{solution}\nÉtablis le plan de monétisation 0 DH.")

    # Rapport Final
    final_report = (
        f"🚨 **MISSION 0 DH : RAPPORT DE CASH ORGANIQUE** 🚨\n\n"
        f"🔥 **1. Le Problème :**\n{problem}\n\n"
        f"🛑 **2. Filtre Anti-Coût (Critique) :**\n{criticism[:300]}...\n\n"
        f"🛠️ **3. Solution 100% Gratuite :**\n{solution}\n\n"
        f"💰 **4. Monétisation & Trafic Organique :**\n{monetization}"
    )

    send_telegram_message(final_report)
    print("--- [MISSION] Rapport 0 DH envoyé ! ---")

if __name__ == "__main__":
    daily_autonomous_mission()
