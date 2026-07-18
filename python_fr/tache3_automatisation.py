# ============================================================
#  TÂCHE 3 — AUTOMATISATION DE TÂCHES AVEC PYTHON
#  CodeAlpha Python Internship
#  Concepts : os, shutil, re, requests, gestion de fichiers
#
#  3 fonctions disponibles (menu au lancement) :
#    A) Déplacer les fichiers .jpg vers un nouveau dossier
#    B) Extraire les e-mails d'un fichier .txt
#    C) Scraper le titre d'une page web
# ============================================================

import os
import shutil
import re
import sys

# ── Importation optionnelle de requests ─────────────────────
try:
    import requests
    REQUESTS_OK = True
except ImportError:
    REQUESTS_OK = False


# ╔══════════════════════════════════════════════════════════╗
# ║  OPTION A — Déplacer les fichiers .jpg                  ║
# ╚══════════════════════════════════════════════════════════╝

def deplacer_jpg(dossier_source: str, dossier_cible: str) -> None:
    """
    Déplace tous les fichiers .jpg (et .jpeg) du dossier source
    vers le dossier cible (créé automatiquement si inexistant).
    """
    # Vérifier que le dossier source existe
    if not os.path.isdir(dossier_source):
        print(f"  ❌ Dossier source introuvable : {dossier_source}")
        return

    # Créer le dossier cible si nécessaire
    os.makedirs(dossier_cible, exist_ok=True)

    # Lister les fichiers .jpg / .jpeg
    fichiers_jpg = [
        f for f in os.listdir(dossier_source)
        if f.lower().endswith((".jpg", ".jpeg"))
        and os.path.isfile(os.path.join(dossier_source, f))
    ]

    if not fichiers_jpg:
        print("  ℹ️  Aucun fichier .jpg trouvé dans le dossier source.")
        return

    print(f"\n  🔍 {len(fichiers_jpg)} fichier(s) .jpg trouvé(s) :\n")
    deplaces = 0
    ignores  = 0

    for nom in fichiers_jpg:
        src  = os.path.join(dossier_source, nom)
        dest = os.path.join(dossier_cible,  nom)

        # Gestion des conflits de nom
        if os.path.exists(dest):
            base, ext = os.path.splitext(nom)
            compteur = 1
            while os.path.exists(dest):
                dest = os.path.join(dossier_cible, f"{base}_{compteur}{ext}")
                compteur += 1
            print(f"  ⚠️  Conflit : {nom} → renommé en {os.path.basename(dest)}")

        shutil.move(src, dest)
        print(f"  ✅ Déplacé : {nom}")
        deplaces += 1

    print(f"\n  📊 Résultat : {deplaces} déplacé(s), {ignores} ignoré(s)")
    print(f"  📁 Dossier cible : {os.path.abspath(dossier_cible)}\n")


# ╔══════════════════════════════════════════════════════════╗
# ║  OPTION B — Extraire les adresses e-mail                ║
# ╚══════════════════════════════════════════════════════════╝

# Expression régulière pour détecter les e-mails
REGEX_EMAIL = re.compile(
    r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}"
)


def extraire_emails(fichier_entree: str, fichier_sortie: str) -> None:
    """
    Lit un fichier .txt, extrait toutes les adresses e-mail uniques
    et les sauvegarde dans un fichier de sortie.
    """
    if not os.path.isfile(fichier_entree):
        print(f"  ❌ Fichier introuvable : {fichier_entree}")
        return

    with open(fichier_entree, "r", encoding="utf-8", errors="ignore") as f:
        contenu = f.read()

    # Extraction avec regex — set() pour éliminer les doublons
    emails_trouves = sorted(set(REGEX_EMAIL.findall(contenu)))

    if not emails_trouves:
        print("  ℹ️  Aucune adresse e-mail trouvée dans le fichier.")
        return

    print(f"\n  📧 {len(emails_trouves)} adresse(s) e-mail trouvée(s) :\n")

    with open(fichier_sortie, "w", encoding="utf-8") as f:
        f.write(f"Adresses e-mail extraites depuis : {fichier_entree}\n")
        f.write(f"Nombre total : {len(emails_trouves)}\n")
        f.write("=" * 50 + "\n\n")
        for email in emails_trouves:
            f.write(email + "\n")
            print(f"  • {email}")

    print(f"\n  ✅ E-mails sauvegardés dans : {os.path.abspath(fichier_sortie)}\n")


# ╔══════════════════════════════════════════════════════════╗
# ║  OPTION C — Scraper le titre d'une page web             ║
# ╚══════════════════════════════════════════════════════════╝

def extraire_titre_html(html: str) -> str:
    """
    Extrait le contenu de la balise <title> dans une chaîne HTML.
    Utilise une regex simple (pas de BeautifulSoup requis).
    """
    match = re.search(r"<title[^>]*>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
    if match:
        # Nettoyer les espaces et sauts de ligne éventuels
        return re.sub(r"\s+", " ", match.group(1)).strip()
    return "(Titre introuvable)"


def scraper_titre(url: str, fichier_sortie: str) -> None:
    """
    Effectue une requête GET sur l'URL donnée, extrait le titre
    de la page HTML et le sauvegarde dans un fichier texte.
    """
    if not REQUESTS_OK:
        print("  ❌ Le module 'requests' n'est pas installé.")
        print("     Exécutez : pip install requests")
        return

    print(f"\n  🌐 Connexion à : {url}")

    try:
        reponse = requests.get(url, timeout=10, headers={
            "User-Agent": "Mozilla/5.0 (CodeAlpha-Bot/1.0)"
        })
        reponse.raise_for_status()
    except requests.exceptions.ConnectionError:
        print("  ❌ Erreur de connexion. Vérifiez votre accès Internet.")
        return
    except requests.exceptions.Timeout:
        print("  ❌ Délai d'attente dépassé (timeout).")
        return
    except requests.exceptions.HTTPError as e:
        print(f"  ❌ Erreur HTTP : {e}")
        return

    titre = extraire_titre_html(reponse.text)
    print(f"  📄 Titre trouvé : {titre}")

    # Sauvegarde dans un fichier
    with open(fichier_sortie, "w", encoding="utf-8") as f:
        f.write(f"URL      : {url}\n")
        f.write(f"Titre    : {titre}\n")
        f.write(f"Statut   : {reponse.status_code} {reponse.reason}\n")

    print(f"  ✅ Titre sauvegardé dans : {os.path.abspath(fichier_sortie)}\n")


# ╔══════════════════════════════════════════════════════════╗
# ║  MENU PRINCIPAL                                         ║
# ╚══════════════════════════════════════════════════════════╝

def menu():
    print("=" * 52)
    print("   🤖  AUTOMATISATION DE TÂCHES — CodeAlpha")
    print("=" * 52)
    print("  Choisissez une option :\n")
    print("  [A] Déplacer les fichiers .jpg vers un dossier")
    print("  [B] Extraire les e-mails d'un fichier .txt")
    print("  [C] Scraper le titre d'une page web")
    print("  [Q] Quitter")
    print()
    return input("  Votre choix : ").strip().upper()


def main():
    choix = menu()

    # ── Option A ─────────────────────────────────────────────
    if choix == "A":
        print("\n  📁 DÉPLACEMENT DE FICHIERS .JPG\n")
        source = input("  Dossier source (ex: C:/Images) : ").strip()
        cible  = input("  Dossier cible  (ex: C:/Images/JPG) : ").strip()
        deplacer_jpg(source, cible)

    # ── Option B ─────────────────────────────────────────────
    elif choix == "B":
        print("\n  📧 EXTRACTION D'ADRESSES E-MAIL\n")
        entree  = input("  Fichier source .txt (ex: contacts.txt) : ").strip()
        sortie  = input("  Fichier de sortie  (ex: emails.txt)    : ").strip()
        extraire_emails(entree, sortie)

    # ── Option C ─────────────────────────────────────────────
    elif choix == "C":
        print("\n  🌐 SCRAPING DU TITRE D'UNE PAGE WEB\n")
        url    = input("  URL de la page (ex: https://example.com) : ").strip()
        sortie = input("  Fichier de sortie (ex: titre.txt)        : ").strip()
        scraper_titre(url, sortie)

    # ── Quitter ───────────────────────────────────────────────
    elif choix == "Q":
        print("\n  👋 Au revoir !\n")
        sys.exit(0)

    else:
        print("\n  ⚠️  Option invalide. Relancez le programme.\n")


if __name__ == "__main__":
    main()
