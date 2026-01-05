from datetime import datetime
from fonction_utilitaire.utilitaire import clear_console
from config import CURSOR, CONN
import mysql.connector
import random

# Afficher une liste d'équipes et permettre à l'utilisateur d'en choisir une
def choisir_equipe_par_liste(equipes, titre="Choisis une équipe"):
    print(f"\n📋 {titre}")
    for i, (id_equipe, nom) in enumerate(equipes, start=1):
        print(f"{i}. {nom} (id={id_equipe})")

    while True:
        choix = input("➡ Numéro (ou Entrée pour annuler): ").strip()
        if choix == "":
            return None
        if choix.isdigit():
            idx = int(choix)
            if 1 <= idx <= len(equipes):
                return equipes[idx - 1][0]
        print("❌ Choix invalide.")


def get_equipes():
    CURSOR.execute("SELECT id_equipe, nom_equipe FROM equipe ORDER BY nom_equipe")
    return CURSOR.fetchall()

# On garantit qu'il existe une ligne dans equipe_adverse pour l'équipe choisie.
def get_or_create_equipe_adverse_id(nom_equipe):
    CURSOR.execute(
        "SELECT id_equipe_adverse FROM equipe_adverse WHERE nom_equipe_adverse = %s",
        (nom_equipe,)
    )
    row = CURSOR.fetchone()
    if row:
        return row[0]

    CURSOR.execute(
        "INSERT INTO equipe_adverse (nom_equipe_adverse, score_equipe_adverse) VALUES (%s, %s)",
        (nom_equipe, 0)
    )
    CONN.commit()
    return CURSOR.lastrowid


def choisir_equipes_match():
    equipes = get_equipes()
    if len(equipes) < 2:
        print("❌ Pas assez d'équipes pour lancer un match (il en faut au moins 2).")
        return None, None

    id_equipe_1 = choisir_equipe_par_liste(equipes, "Choisis l'équipe 1")
    if id_equipe_1 is None:
        return None, None

    equipes_restantes = [(i, n) for (i, n) in equipes if i != id_equipe_1]
    id_equipe_2 = choisir_equipe_par_liste(equipes_restantes, "Choisis l'équipe 2")
    if id_equipe_2 is None:
        return None, None

    nom_equipe_2 = next(n for (i, n) in equipes if i == id_equipe_2)
    id_equipe_adverse = get_or_create_equipe_adverse_id(nom_equipe_2)

    return id_equipe_1, id_equipe_adverse


def saisir_score():
    while True:
        s1 = input("⚽ Score équipe 1: ").strip()
        s2 = input("⚽ Score équipe 2: ").strip()
        if s1.isdigit() and s2.isdigit():
            return int(s1), int(s2)
        print("❌ Saisie invalide. Mets des nombres entiers (ex: 2 et 1).")

# Enregistrer le match dans la base de données, lorsqu'il on enregistre un match deja joué aujourd'hui entre les mêmes équipes, on affiche le message de refus
def enregistrer_match(id_equipe, id_equipe_adverse, score1, score2):
    date_match = datetime.now().date().isoformat()

    try:
        CURSOR.execute("""
            INSERT INTO `match`
            (id_equipe, id_equipe_adverse, date_match, score_equipe, score_adverse)
            VALUES (%s, %s, %s, %s, %s)
        """, (id_equipe, id_equipe_adverse, date_match, score1, score2))

        CONN.commit()

    except mysql.connector.errors.IntegrityError:
        CURSOR.execute("""
            SELECT score_equipe, score_adverse
            FROM `match`
            WHERE id_equipe = %s
              AND id_equipe_adverse = %s
              AND date_match = %s
        """, (id_equipe, id_equipe_adverse, date_match))

        match_existant = CURSOR.fetchone()

        print("\n❌ MATCH REFUSÉ (déjà enregistré aujourd’hui)")
        if match_existant:
            s1, s2 = match_existant
            print("📊 Score déjà enregistré :")
            print(f"--->| {s1} - {s2} |<---")
        else:
            print("⚠️ Match existant, mais score introuvable.")

        input("\n👈 Appuyez sur Entrée pour continuer...")
        return False
    
    return True

# on a 30% de chance qu'un joueur non blessé se blesse lors d'un match
def appliquer_blessures(id_equipe, proba=0.3):
    CURSOR.execute("""
        SELECT j.id_joueur
        FROM joueur j
        JOIN equipe_joueur ej ON ej.id_joueur = j.id_joueur
        WHERE ej.id_equipe = %s
          AND j.blessure_joueur = 0
    """, (id_equipe,))

    joueurs = CURSOR.fetchall()

    for (id_joueur,) in joueurs:
        if random.random() < proba:
            CURSOR.execute("""
                UPDATE joueur
                SET blessure_joueur = 1
                WHERE id_joueur = %s
            """, (id_joueur,))
            print(f"🚑 Joueur {id_joueur} blessé")

    CONN.commit()

# Fonction principale pour jouer un match, 
# quand on enregistre un match déjà joué aujourd'hui entre les mêmes équipes, 
# on affiche le message de refus avec l'ettat de match
def jouer_match():
    clear_console()

    id_equipe_1, id_equipe_adverse = choisir_equipes_match()
    if id_equipe_1 is None:
        return

    print("\n🏁 Match en cours...")
    score1, score2 = saisir_score()

    condition_correct = enregistrer_match(id_equipe_1, id_equipe_adverse, score1, score2)

    # pour que le reste du code ne s'exécute pas si le match n'a pas été enregistré
    if not condition_correct:
        return

    appliquer_blessures(id_equipe_1)

    print("\n✅ Match terminé et enregistré !")
    print(f"📊 Résultat : {score1} - {score2}")
    input("\n👈 Appuyez sur Entrée pour continuer...")


def afficher_historique_matchs(limit=50):
    clear_console()
    print("📜 Historique des matchs\n")

    limit = int(limit)

    CURSOR.execute(f"""
        SELECT
            m.date_match,
            e.nom_equipe AS equipe_1,
            ea.nom_equipe_adverse AS equipe_2,
            m.score_equipe,
            m.score_adverse
        FROM `match` m
        JOIN equipe e ON e.id_equipe = m.id_equipe
        JOIN equipe_adverse ea ON ea.id_equipe_adverse = m.id_equipe_adverse
        ORDER BY m.date_match DESC
        LIMIT {limit}
    """)

    rows = CURSOR.fetchall()
    if not rows:
        print("Aucun match enregistré.")
        input("\n👈 Entrée pour revenir...")
        return

    for (date_m, eq1, eq2, s1, s2) in rows:
        print(f"🗓 {date_m} | {eq1} {s1} - {s2} {eq2}")

    input("\n👈 Entrée pour revenir...")
