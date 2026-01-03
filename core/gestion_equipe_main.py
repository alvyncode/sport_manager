from fonction_utilitaire.utilitaire import *
from config import *
from tabulate import tabulate
import random
from core.changement_de_config import*

def calculer_score_joueur(vitesse, technique, force, endurance, poste):
    coeffs = {
        "Attaquant": {"v": 0.35, "t": 0.40, "f": 0.10, "e": 0.15},
        "Milieu": {"v": 0.25, "t": 0.30, "f": 0.20, "e": 0.25},
        "Défenseur": {"v": 0.15, "t": 0.15, "f": 0.40, "e": 0.30},
        "Gardien": {"v": 0.10, "t": 0.30, "f": 0.30, "e": 0.30}
    }
    c = coeffs.get(poste, {"v": 0.25, "t": 0.25, "f": 0.25, "e": 0.25})
    score = vitesse*c["v"] + technique*c["t"] + force*c["f"] + endurance*c["e"]
    return round(score, 1)

def update_score_joueur(id_joueur):
    # Il faut faire un JOIN pour récupérer le poste
    sql = """SELECT j.vitesse_joueur, j.score_technique_joueur, 
                    j.force_joueur, j.endurance_joueur, ej.poste
             FROM joueur j
             JOIN equipe_joueur ej ON j.id_joueur = ej.id_joueur
             WHERE j.id_joueur = %s"""
    
    CURSOR.execute(sql, (id_joueur,))
    result = CURSOR.fetchone()
    
    if result:
        vitesse, technique, force, endurance, poste = result
        score = calculer_score_joueur(vitesse, technique, force, endurance, poste)
        CURSOR.execute("UPDATE joueur SET score_joueur = %s WHERE id_joueur = %s", (score, id_joueur))
        CONN.commit()
    
def calculer_score_equipe(id_equipe):
    CURSOR.execute("""
    SELECT SUM(j.score_joueur)
    FROM joueur j
    JOIN equipe_joueur ej ON j.id_joueur = ej.id_joueur
    WHERE ej.id_equipe = %s AND ej.titre_joueur = 'Titulaire'
    """, (id_equipe,))
    total_score = CURSOR.fetchone()[0]
    return total_score if total_score is not None else 0

def update_score_equipe(id_equipe):
    total_score = calculer_score_equipe(id_equipe)
    CURSOR.execute("UPDATE equipe SET score_equipe = %s WHERE id_equipe = %s", (total_score, id_equipe))
    CONN.commit()

def afficher_joueurs_disponibles():
    sql = "SELECT id_joueur, nom_joueur, prenom_joueur, score_joueur, vitesse_joueur, score_technique_joueur, force_joueur, endurance_joueur, blessure_joueur FROM joueur WHERE score_joueur is NOT NUll"
    CURSOR.execute(sql)
    result = CURSOR.fetchall()
    if result:
        headers = ["ID", "Nom", "Prénom","Score", "Vitesse", "Score Technique", "Force", "Endurance", "Blessure"]
        table = [list(row) for row in result]
        print("Joueurs Disponibles :")
        print(tabulate(table, headers, tablefmt="grid"))
    else:
        print("Aucun joueur disponible trouvé.")

    if input():
        return 

def ajouter_joueur_manuellement() -> int: #Fonction d'ajout manuel de joueur
    def demander_competence(message, min_val=0, max_val=100):
        valeur = int(input(message))
        if not min_val <= valeur <= max_val:
            raise ValueError(f"La valeur doit être entre {min_val} et {max_val}")
        return valeur
    try :
        nom = str(input("Nom du joueur : "))
        prenom = str(input("Prénom du joueur : "))
        vitesse = demander_competence("Vitesse (0-100) : ")
        score_technique = demander_competence("Score Technique (0-100) :    ")
        force = demander_competence("Force (0-100) : ")
        endurance = demander_competence("Endurance (0-100) : ")
        sql = "INSERT INTO joueur (nom_joueur, prenom_joueur, vitesse_joueur, score_technique_joueur, force_joueur, endurance_joueur,blessure_joueur) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (nom, prenom, vitesse, score_technique,force,endurance,0)
        CURSOR.execute(sql, val)
        CONN.commit()
        return int(CURSOR.lastrowid)
    except ValueError or mysql.connector.errors.ProgrammingError:
        print("Il semblerait qu'une erreur s'est produite. Veuillez réessayer.")
        ajouter_joueur_manuellement()

def faire_confiance_au_selectionneur() -> None: #Fonction d'ajout de joueur par algorithme (Aléatoirement)
    def definir_nom_prenom_aleatoire()->tuple:#definir nom et prenom aléatoire grace a une table de nom et prenom prédéfinie
        CURSOR.execute("SELECT nom, prenom FROM nom_prenom_r ORDER BY RAND() LIMIT 1")
        resultat = CURSOR.fetchone()
        if resultat is None:
            raise Exception("Aucun nom/prénom trouvé dans la table nom_prenom_r")
        nom, prenom = resultat
        return nom, prenom
    def competances_aleatoires():
        vitesse = int(random.triangular(0,100,65))
        score_technique = int(random.triangular(0,100,65))
        force = int(random.triangular(0,100,65))
        endurance = int(random.triangular(0,100,65))
        return vitesse, score_technique, force, endurance
    try:
        nom, prenom = definir_nom_prenom_aleatoire()
        vitesse, score_technique, force, endurance = competances_aleatoires()
        sql = "INSERT INTO joueur (nom_joueur, prenom_joueur, vitesse_joueur, score_technique_joueur, force_joueur, endurance_joueur,blessure_joueur) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (nom, prenom, vitesse, score_technique,force,endurance,0)
        CURSOR.execute(sql, val)
        CONN.commit()
        return CURSOR.lastrowid
    except ValueError or mysql.connector.errors.ProgrammingError:
        print("Il semblerait qu'une erreur s'est produite. Veuillez réessayer.")
        faire_confiance_au_selectionneur()

def recruter_joueur(): #Fonction principale de recrutement des joueurs(main)
    clear_console()
    afficher_txt(CHOIX_AJOUT_JOUEUR)
    user_choice = choix_interface(3)
    if user_choice == '1': #Ajout manuel
        id_joueur = ajouter_joueur_manuellement()
        CONN.commit()
        id_equipe = creation_connexion_equipe()
        CONN.commit()
        CURSOR.execute("INSERT INTO equipe_joueur (id_equipe, id_joueur,poste,titre_joueur) VALUES(%s,%s,%s,%s)",(id_equipe,id_joueur,poste(),"Réserviste"))
        CONN.commit()
        update_score_joueur(id_joueur)
        update_score_equipe(id_equipe)
    elif user_choice == '2': #Ajout par algorithme
        id_joueur = faire_confiance_au_selectionneur()
        id_equipe = choisir_equipe()
        poste_joueur = poste()  # DEMANDER le poste
        CURSOR.execute("INSERT INTO equipe_joueur(id_joueur, id_equipe, poste, titre_joueur) VALUES(%s,%s,%s,%s)",
                       (id_joueur, id_equipe, poste_joueur, "Réserviste"))
        CONN.commit()
        update_score_joueur(id_joueur)
        update_score_equipe(id_equipe)
    elif user_choice == '3': #Voir liste des joueurs ajoutés
        afficher_joueurs_disponibles()
    elif user_choice in ['X', 'x']:
        print("Retour au menu de gestion de l'équipe.")

def gestion_equipe():
    clear_console()
    afficher_txt(MENU_GESTION_EQUIPE)
    user_choice = choix_interface(3)
    if user_choice == '1':#Recruter un joueur
        recruter_joueur()
    elif user_choice == '2':#configuration-mise en place des titulaires, ajout et modification de poste/
        changer_configuration()
    elif user_choice == '3':#afficher les joueurs inséré dans la BDD
        clear_console()
        afficher_joueurs_disponibles()
        if input("Entrer pour quitter : ") == "" :
            gestion_equipe()
