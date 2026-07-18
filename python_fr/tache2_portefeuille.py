# ============================================================
#  TÂCHE 2 — TRACKER DE PORTEFEUILLE BOURSIER
#  CodeAlpha Python Internship
#  Concepts : dictionnaire, I/O, arithmétique, fichiers
# ============================================================

import csv
import os
from datetime import datetime

# ── Prix des actions (dictionnaire figé en USD) ──────────────
PRIX_ACTIONS = {
    "AAPL":  182.50,   # Apple
    "TSLA":  248.00,   # Tesla
    "GOOGL": 175.30,   # Alphabet (Google)
    "MSFT":  415.20,   # Microsoft
    "AMZN":  189.90,   # Amazon
    "META":  502.10,   # Meta (Facebook)
    "NVDA":  875.40,   # NVIDIA
    "NFLX":  635.00,   # Netflix
}

FICHIER_CSV = "portefeuille.csv"
FICHIER_TXT = "portefeuille.txt"


# ── Fonctions utilitaires ────────────────────────────────────

def afficher_actions_disponibles():
    """Affiche la liste des actions disponibles avec leur prix."""
    print("\n  📈 Actions disponibles :")
    print("  " + "─" * 38)
    print(f"  {'Symbole':<10} {'Nom':<20} {'Prix (USD)':>8}")
    print("  " + "─" * 38)
    noms = {
        "AAPL": "Apple", "TSLA": "Tesla", "GOOGL": "Alphabet",
        "MSFT": "Microsoft", "AMZN": "Amazon", "META": "Meta",
        "NVDA": "NVIDIA", "NFLX": "Netflix",
    }
    for symbole, prix in PRIX_ACTIONS.items():
        print(f"  {symbole:<10} {noms[symbole]:<20} {prix:>8.2f} $")
    print("  " + "─" * 38)


def saisir_portefeuille():
    """
    Demande à l'utilisateur de saisir ses actions et quantités.
    Retourne un dictionnaire {symbole: quantite}.
    """
    portefeuille = {}
    print("\n  📝 Saisissez vos actions (tapez 'fin' pour terminer)\n")

    while True:
        symbole = input("  Symbole de l'action : ").strip().upper()

        if symbole == "FIN":
            break

        if symbole not in PRIX_ACTIONS:
            print(f"  ⚠️  '{symbole}' n'est pas disponible. Choisissez parmi la liste.\n")
            continue

        # Saisie de la quantité
        while True:
            try:
                qte = int(input(f"  Quantité de {symbole} : ").strip())
                if qte <= 0:
                    print("  ⚠️  La quantité doit être un entier positif.")
                    continue
                break
            except ValueError:
                print("  ⚠️  Veuillez entrer un nombre entier valide.")

        # Ajouter ou cumuler
        if symbole in portefeuille:
            portefeuille[symbole] += qte
            print(f"  ✅ Mis à jour : {symbole} → {portefeuille[symbole]} actions\n")
        else:
            portefeuille[symbole] = qte
            print(f"  ✅ Ajouté : {symbole} × {qte}\n")

    return portefeuille


def calculer_valeurs(portefeuille):
    """
    Calcule la valeur par ligne et le total.
    Retourne une liste de tuples (symbole, quantite, prix, valeur).
    """
    lignes = []
    for symbole, qte in portefeuille.items():
        prix   = PRIX_ACTIONS[symbole]
        valeur = prix * qte
        lignes.append((symbole, qte, prix, valeur))
    return lignes


def afficher_rapport(lignes):
    """Affiche le rapport de portefeuille dans la console."""
    total = sum(v for _, _, _, v in lignes)
    horodatage = datetime.now().strftime("%d/%m/%Y %H:%M")

    print()
    print("  " + "═" * 56)
    print("        💼  RAPPORT DE PORTEFEUILLE BOURSIER")
    print(f"        📅  {horodatage}")
    print("  " + "═" * 56)
    print(f"  {'Symbole':<10} {'Qté':>6}  {'Prix unit.':>12}  {'Valeur':>13}")
    print("  " + "─" * 56)

    for symbole, qte, prix, valeur in lignes:
        print(f"  {symbole:<10} {qte:>6}  {prix:>10.2f} $  {valeur:>11.2f} $")

    print("  " + "─" * 56)
    print(f"  {'TOTAL':>36}  {total:>11.2f} $")
    print("  " + "═" * 56)
    print(f"\n  💰 Valeur totale de votre portefeuille : {total:,.2f} USD\n")

    return total, horodatage


def sauvegarder_csv(lignes, total, horodatage):
    """Sauvegarde le portefeuille dans un fichier CSV."""
    with open(FICHIER_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Date", "Symbole", "Quantité", "Prix unitaire (USD)", "Valeur (USD)"])
        for symbole, qte, prix, valeur in lignes:
            writer.writerow([horodatage, symbole, qte, f"{prix:.2f}", f"{valeur:.2f}"])
        writer.writerow([])
        writer.writerow(["", "", "", "TOTAL", f"{total:.2f}"])
    print(f"  📄 Sauvegardé en CSV  → {os.path.abspath(FICHIER_CSV)}")


def sauvegarder_txt(lignes, total, horodatage):
    """Sauvegarde le portefeuille dans un fichier texte lisible."""
    with open(FICHIER_TXT, "w", encoding="utf-8") as f:
        f.write("=" * 56 + "\n")
        f.write("   RAPPORT DE PORTEFEUILLE BOURSIER\n")
        f.write(f"   Date : {horodatage}\n")
        f.write("=" * 56 + "\n")
        f.write(f"{'Symbole':<10} {'Qté':>6}  {'Prix unit.':>12}  {'Valeur':>13}\n")
        f.write("-" * 56 + "\n")
        for symbole, qte, prix, valeur in lignes:
            f.write(f"{symbole:<10} {qte:>6}  {prix:>10.2f} $  {valeur:>11.2f} $\n")
        f.write("-" * 56 + "\n")
        f.write(f"{'TOTAL':>36}  {total:>11.2f} $\n")
        f.write("=" * 56 + "\n")
    print(f"  📄 Sauvegardé en TXT  → {os.path.abspath(FICHIER_TXT)}")


def main():
    print("=" * 56)
    print("   📊  TRACKER DE PORTEFEUILLE BOURSIER — CodeAlpha")
    print("=" * 56)

    # Afficher les actions disponibles
    afficher_actions_disponibles()

    # Saisie du portefeuille
    portefeuille = saisir_portefeuille()

    if not portefeuille:
        print("\n  ⚠️  Aucune action saisie. Fin du programme.\n")
        return

    # Calcul et affichage
    lignes = calculer_valeurs(portefeuille)
    total, horodatage = afficher_rapport(lignes)

    # Sauvegarde optionnelle
    choix = input("  💾 Sauvegarder le résultat ? (csv / txt / les deux / non) : ").strip().lower()
    print()
    if choix in ("csv", "les deux"):
        sauvegarder_csv(lignes, total, horodatage)
    if choix in ("txt", "les deux"):
        sauvegarder_txt(lignes, total, horodatage)
    if choix == "non":
        print("  ℹ️  Résultat non sauvegardé.")

    print("\n  ✅ Programme terminé. Bonne gestion de votre portefeuille !\n")


if __name__ == "__main__":
    main()
