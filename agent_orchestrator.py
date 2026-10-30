import os
import time
from datetime import datetime
from google import genai
from google.genai import types

# Initialisation du client (lit automatiquement GEMINI_API_KEY depuis l'environnement)
client = genai.Client()

def call_agent(role_instruction, prompt_input, max_retries=3, retry_delay=6):
    """Appelle l'agent avec un système de réessai automatique en cas de surcharge."""
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model='gemini-3.8-flash',
                contents=prompt_input,
                config=types.GenerateContentConfig(
                    system_instruction=role_instruction,
                    temperature=0.85,
                ),
            )
            return response.text
        except Exception as e:
            print(f"⚠️ Tentative {attempt + 1}/{max_retries} échouée : {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)  # Attend quelques secondes avant de relancer
            else:
                return f"Erreur lors de l'appel à l'agent après {max_retries} tentatives : {str(e)}"

def save_report_to_file(report_content):
    # Crée le dossier 'reports' s'il n'existe pas
    os.makedirs("reports", exist_ok=True)
    
    # Nom du fichier basé sur la date et l'heure
    date_str = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"reports/rapport_{date_str}.md"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(report_content)
        
    print(f">> Rapport sauvegardé avec succès dans le fichier : {filename}")

def daily_autonomous_mission():
    print("--- [MISSION 0 DH] Démarrage des agents (Modèle 3.8-flash & Blindé) ---")
    
    # 1. Explorateur de Problèmes
    explorer_prompt = (
        "Tu es un expert en veille et opportunités digitales à ZERO BUDGET. "
        "Identifie UN problème urgent et actuel sur internet où les gens galèrent, "
        "mais pour lequel ils recherchent des astuces ou des outils gratuits."
    )
    problem = call_agent(explorer_prompt, "Trouve un pain-point brûlant du moment sur le web.")
    time.sleep(4) # Pause de courtoisie pour l'API
    
    # 2. Agent Critique (Chasse aux coûts cachés)
    critic_prompt = (
        "Tu es l'agent critique intraitable sur le budget. "
        "Vérifie le problème trouvé : si la solution demande le moindre centime d'investissement (pub, hébergement payant, outil pro), "
        "détruis l'idée. On ne veut que du 0 dirham."
    )
    criticism = call_agent(critic_prompt, f"Problème :\n{problem}\nAnalyse les risques de coûts cachés.")
    time.sleep(4)

    # 3. Concepteur de Solution (100% Gratuit)
    solution_prompt = (
        "Conçois une solution qui coûte exactement 0 dirham à créer et déployer "
        "(ex: script Python gratuit sur GitHub, template partagé via Google Sheets/Notion gratuit, "
        "site hébergé gratuitement sur Netlify/GitHub Pages, ou contenu organique sur les réseaux)."
    )
    solution = call_agent(solution_prompt, f"Problème :\n{problem}\nCritique :\n{criticism}\nPropose la solution technique 100% gratuite.")
    time.sleep(4)

    # 4. Stratège en Monétisation Organique
    monetization_prompt = (
        "Comment monétiser cette solution gratuitement ? "
        "Exemples : liens d'affiliation (Amazon, 0 DH), dons (Ko-fi/Buy Me a Coffee), "
        "ou vente de services de mise en place directe via démarchage organique sur les réseaux sociaux. "
        "Donne le plan d'action d'acquisition 100% organique (sans un seul centime de pub)."
    )
    monetization = call_agent(monetization_prompt, f"Solution :\n{solution}\nÉtablis le plan de monétisation 0 DH.")

    # Rapport Final Formaté Markdown pour GitHub
    final_report = (
        f"# 🚨 MISSION 0 DH : RAPPORT DE CASH\n"
        f"**Date :** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        f"## 🔥 1. Le Problème\n{problem}\n\n"
        f"## 🛑 2. Filtre Anti-Coût (Critique)\n{criticism}\n\n"
        f"## 🛠️ 3. Solution 100% Gratuite\n{solution}\n\n"
        f"## 💰 4. Monétisation & Trafic\n{monetization}\n"
    )

    # Sauvegarde du rapport localement dans le dépôt
    save_report_to_file(final_report)
    print("--- [MISSION] Rapport sauvegardé dans le dépôt avec succès ! ---")

if __name__ == "__main__":
    daily_autonomous_mission()
