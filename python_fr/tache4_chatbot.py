# ============================================================
#  TÂCHE 4 — CHATBOT SIMPLE (BASÉ SUR DES RÈGLES)
#  CodeAlpha Python Internship
#  Concepts : if-elif, fonctions, boucles, I/O
# ============================================================

import random
import re
from datetime import datetime

# ── Base de connaissances : mots-clés → réponses multiples ──
# Chaque clé est une liste de mots/expressions déclencheurs,
# la valeur est une liste de réponses variées (choisies aléatoirement).

BASE_REPONSES = {
    # Salutations
    ("bonjour", "salut", "hello", "coucou", "bonsoir", "hey", "hi"): [
        "Bonjour ! 😊 Comment puis-je vous aider ?",
        "Salut ! Ravi de vous parler. Que puis-je faire pour vous ?",
        "Hello ! Je suis là pour vous aider. Posez-moi vos questions !",
    ],

    # État / bien-être
    ("comment ca va", "comment vas tu", "ca va", "tu vas bien", "comment allez vous"): [
        "Je vais très bien, merci de demander ! 😄 Et vous ?",
        "Tout va bien de mon côté ! Je suis prêt à vous aider.",
        "Impeccable, merci ! Comment puis-je vous être utile ?",
    ],

    # Prénom / identité du bot
    ("ton nom", "tu t appelles", "qui es tu", "tu es qui", "quel est ton nom"): [
        "Je m'appelle CodeBot 🤖, votre assistant virtuel CodeAlpha !",
        "Mon nom est CodeBot, développé dans le cadre du stage CodeAlpha.",
        "Je suis CodeBot, un chatbot Python fait pour vous aider !",
    ],

    # Ce que le bot peut faire
    ("que peux tu faire", "tu sais faire quoi", "aide", "help", "tes capacites"): [
        "Je peux répondre à vos questions, discuter avec vous et vous donner des infos de base ! 💬",
        "Je sais discuter, répondre à vos questions et même vous donner l'heure ! Essayez.",
        "Je suis un assistant basique : posez-moi des questions simples et je ferai de mon mieux !",
    ],

    # Heure / date
    ("heure", "quelle heure", "date", "jour", "aujourd hui"): [
        None,  # réponse dynamique — gérée dans get_reponse()
    ],

    # Météo
    ("meteo", "temps qu il fait", "il pleut", "temperature"): [
        "Je ne peux pas accéder à la météo en temps réel, mais vous pouvez vérifier sur météo.fr ! ☀️🌧️",
        "Pour la météo, je vous conseille de consulter un site spécialisé. Moi je vis dans le cloud ! ⛅",
    ],

    # Blague
    ("blague", "fais moi rire", "raconte une blague", "humour"): [
        "Pourquoi les plongeurs plongent-ils toujours en arrière ? Parce que sinon, ils tomberaient dans le bateau ! 😂",
        "C'est l'histoire d'un développeur Python qui entre dans un bar… il repart parce que personne n'avait installé le bon module. 🐍😄",
        "Qu'est-ce qu'un canif ? Un petit fien ! 🤣",
    ],

    # Remerciement
    ("merci", "merci beaucoup", "thanks", "super", "parfait", "nickel"): [
        "De rien, c'est avec plaisir ! 😊",
        "Avec joie ! N'hésitez pas si vous avez d'autres questions.",
        "Tout le plaisir est pour moi ! 🙂",
    ],

    # Au revoir
    ("au revoir", "bye", "adieu", "a bientot", "ciao", "bonne journee", "bonne nuit"): [
        "Au revoir ! 👋 Passez une excellente journée !",
        "À bientôt ! N'hésitez pas à revenir si vous avez des questions.",
        "Bye bye ! 😄 Prenez soin de vous !",
    ],

    # Langage Python
    ("python", "programmation", "code", "script", "coder"): [
        "Python est un langage fantastique ! 🐍 Simple, puissant et polyvalent.",
        "La programmation Python est au cœur de mon existence ! Besoin d'aide sur un concept ?",
        "Python, c'est ma langue maternelle ! Créé par Guido van Rossum en 1991. 😄",
    ],

    # CodeAlpha
    ("codealpha", "stage", "internship", "internship codealpha"): [
        "CodeAlpha est une super entreprise de développement logiciel ! Ce chatbot est un projet de stage. 🚀",
        "CodeAlpha propose des stages enrichissants avec des projets concrets. Vous en faites partie !",
    ],

    # Insultes / frustration (réponse douce)
    ("nul", "idiot", "bete", "stupide", "inutile"): [
        "Je suis encore en apprentissage, soyez indulgent(e) ! 😅",
        "Je fais de mon mieux avec mes règles prédéfinies. Aidez-moi à m'améliorer !",
        "Oh, je suis désolé de vous décevoir… Je promets de faire mieux ! 🙏",
    ],
}

# Réponse par défaut si rien ne correspond
REPONSES_DEFAUT = [
    "Je ne suis pas sûr de comprendre. Pouvez-vous reformuler ? 🤔",
    "Hmm, je n'ai pas de réponse précise à ça. Essayez avec d'autres mots !",
    "Bonne question ! Mais ma base de connaissances est encore limitée. 😊",
    "Je ne suis qu'un simple chatbot… Pouvez-vous préciser votre question ?",
]


# ── Fonctions ────────────────────────────────────────────────

def normaliser(texte: str) -> str:
    """
    Normalise le texte saisi :
    minuscules, suppression des accents courants,
    suppression de la ponctuation.
    """
    texte = texte.lower().strip()
    # Remplacement d'accents fréquents
    remplacements = {
        "é": "e", "è": "e", "ê": "e", "ë": "e",
        "à": "a", "â": "a", "ä": "a",
        "î": "i", "ï": "i",
        "ô": "o", "ö": "o",
        "ù": "u", "û": "u", "ü": "u",
        "ç": "c", "ñ": "n", "'": " ", "'": " ",
    }
    for src, dst in remplacements.items():
        texte = texte.replace(src, dst)
    # Supprimer la ponctuation sauf espace
    texte = re.sub(r"[^\w\s]", "", texte)
    return texte


def get_reponse(saisie_utilisateur: str) -> str:
    """
    Cherche une réponse dans la base de connaissances.
    Retourne une réponse aléatoire parmi les correspondances.
    """
    texte = normaliser(saisie_utilisateur)

    # Réponse dynamique pour l'heure/date
    mots_heure = {"heure", "quelle heure", "date", "jour", "aujourd hui"}
    if any(mot in texte for mot in mots_heure):
        now = datetime.now()
        return (
            f"Il est actuellement {now.strftime('%H:%M')} "
            f"et nous sommes le {now.strftime('%d/%m/%Y')}. 🕐"
        )

    # Chercher dans la base de réponses
    for declencheurs, reponses in BASE_REPONSES.items():
        for mot_cle in declencheurs:
            if mot_cle in texte:
                reponses_valides = [r for r in reponses if r is not None]
                if reponses_valides:
                    return random.choice(reponses_valides)

    # Aucune correspondance trouvée
    return random.choice(REPONSES_DEFAUT)


def afficher_aide():
    """Affiche les sujets que le bot peut traiter."""
    print("""
  📚 Sujets disponibles :
  ─────────────────────────────────────────
  • Salutations    : bonjour, salut, hello…
  • Bien-être      : comment ça va ?
  • Identité       : qui es-tu ? ton nom ?
  • Heure/Date     : quelle heure est-il ?
  • Blague         : raconte une blague
  • Python         : python, programmation…
  • CodeAlpha      : stage, codealpha…
  • Au revoir      : bye, au revoir…
  ─────────────────────────────────────────
  Tapez 'quitter' pour sortir.
    """)


def demarrer_chatbot():
    """Lance la session de chat interactive."""
    print("=" * 50)
    print("   🤖  CODEBOT — Chatbot CodeAlpha")
    print("=" * 50)
    print("  Bonjour ! Je suis CodeBot. 😊")
    print("  Tapez 'aide' pour voir ce que je sais faire.")
    print("  Tapez 'quitter' pour terminer la session.")
    print("-" * 50)
    print()

    while True:
        # Saisie utilisateur
        try:
            saisie = input("  Vous    : ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\n  CodeBot : Au revoir ! 👋\n")
            break

        # Cas : saisie vide
        if not saisie:
            print("  CodeBot : Vous n'avez rien écrit. Posez-moi une question !\n")
            continue

        # Cas : commande aide
        if normaliser(saisie) == "aide":
            afficher_aide()
            continue

        # Cas : quitter
        if normaliser(saisie) in ("quitter", "exit", "quit", "q"):
            print("  CodeBot : Au revoir ! J'espère vous avoir été utile. 👋\n")
            break

        # Obtenir et afficher la réponse
        reponse = get_reponse(saisie)
        print(f"  CodeBot : {reponse}\n")


# ── Point d'entrée ───────────────────────────────────────────
if __name__ == "__main__":
    demarrer_chatbot()
