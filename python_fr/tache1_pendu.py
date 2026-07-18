# ============================================================
#  TÂCHE 1 — JEU DU PENDU
#  CodeAlpha Python Internship
#  Concepts : random, while, if-else, strings, lists
# ============================================================

import random

# ── Liste de mots prédéfinis ─────────────────────────────────
MOTS = ["python", "clavier", "fenetre", "langage", "boucle"]

# ── Dessins du pendu (7 étapes : 0 erreur → 6 erreurs) ──────
PENDU = [
    """
       ┌──────┐
       │      │
              │
              │
              │
              │
    ══════════╧══
    """,
    """
       ┌──────┐
       │      │
       O      │
              │
              │
              │
    ══════════╧══
    """,
    """
       ┌──────┐
       │      │
       O      │
       │      │
              │
              │
    ══════════╧══
    """,
    """
       ┌──────┐
       │      │
       O      │
      /│      │
              │
              │
    ══════════╧══
    """,
    """
       ┌──────┐
       │      │
       O      │
      /│\\     │
              │
              │
    ══════════╧══
    """,
    """
       ┌──────┐
       │      │
       O      │
      /│\\     │
      /       │
              │
    ══════════╧══
    """,
    """
       ┌──────┐
       │      │
       O      │
      /│\\     │
      / \\     │
              │
    ══════════╧══
    """,
]

MAX_ERREURS = 6


def afficher_mot(mot_secret, lettres_trouvees):
    """Affiche le mot avec les lettres devinées et '_' pour les autres."""
    affichage = ""
    for lettre in mot_secret:
        if lettre in lettres_trouvees:
            affichage += lettre + " "
        else:
            affichage += "_ "
    return affichage.strip()


def mot_devine(mot_secret, lettres_trouvees):
    """Retourne True si toutes les lettres du mot ont été trouvées."""
    return all(lettre in lettres_trouvees for lettre in mot_secret)


def jouer():
    """Fonction principale du jeu du Pendu."""
    print("=" * 45)
    print("       🎮  BIENVENUE AU JEU DU PENDU  🎮")
    print("=" * 45)

    # Choisir un mot aléatoire
    mot_secret = random.choice(MOTS)
    lettres_trouvees = []   # lettres correctement devinées
    mauvaises_lettres = []  # lettres incorrectes
    nb_erreurs = 0

    print(f"\nJ'ai choisi un mot de {len(mot_secret)} lettres. Bonne chance !\n")

    # ── Boucle principale du jeu ─────────────────────────────
    while nb_erreurs < MAX_ERREURS:
        # Afficher le dessin du pendu
        print(PENDU[nb_erreurs])

        # Afficher l'état du mot
        print(f"  Mot    : {afficher_mot(mot_secret, lettres_trouvees)}")
        print(f"  Erreurs: {nb_erreurs}/{MAX_ERREURS}")
        print(f"  Mauvaises lettres : {' '.join(mauvaises_lettres) if mauvaises_lettres else '—'}")
        print()

        # Demander une lettre
        saisie = input("  👉 Entrez une lettre : ").strip().lower()

        # Validation de la saisie
        if len(saisie) != 1 or not saisie.isalpha():
            print("  ⚠️  Veuillez entrer une seule lettre.\n")
            continue

        if saisie in lettres_trouvees or saisie in mauvaises_lettres:
            print("  ⚠️  Vous avez déjà proposé cette lettre.\n")
            continue

        # Vérifier si la lettre est dans le mot
        if saisie in mot_secret:
            lettres_trouvees.append(saisie)
            print(f"  ✅ Bien joué ! '{saisie}' est dans le mot.\n")

            # Vérifier si le mot est entièrement deviné
            if mot_devine(mot_secret, lettres_trouvees):
                print(PENDU[nb_erreurs])
                print(f"  🎉 BRAVO ! Vous avez trouvé le mot : « {mot_secret.upper()} »")
                print("=" * 45)
                break
        else:
            mauvaises_lettres.append(saisie)
            nb_erreurs += 1
            print(f"  ❌ '{saisie}' n'est pas dans le mot. ({nb_erreurs}/{MAX_ERREURS})\n")

    else:
        # Le joueur a épuisé ses tentatives
        print(PENDU[MAX_ERREURS])
        print(f"  💀 PERDU ! Le mot était : « {mot_secret.upper()} »")
        print("=" * 45)


def main():
    """Boucle permettant de rejouer."""
    while True:
        jouer()
        rejouer = input("\n🔄 Voulez-vous rejouer ? (o/n) : ").strip().lower()
        if rejouer != "o":
            print("\n👋 Merci d'avoir joué. À bientôt !\n")
            break
        print()


if __name__ == "__main__":
    main()
