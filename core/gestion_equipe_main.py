from fonction_utilitaire.utilitaire import *
from config import *
from tabulate import tabulate

def afficher_joueurs_disponibles():
    sql = "SELECT id_joueur, nom_joueur, prenom_joueur,vitesse_joueur, score_technique_joueur, force_joueur, endurance_joueur FROM joueur WHERE score_joueur is NOT NUll"
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
        return CURSOR.lastrowid
    except ValueError or mysql.connector.errors.ProgrammingError:
        print("Il semblerait qu'une erreur s'est produite. Veuillez réessayer.")
        ajouter_joueur_manuellement()

def faire_confiance_au_selectionneur() ->None: #Fonction d'ajout de joueur par algorithme (Aléatoirement)
    pass

def recruter_joueur(): #Fonction principale de recrutement des joueurs(main)
    clear_console()
    afficher_txt(CHOIX_AJOUT_JOUEUR)
    user_choice = choix_interface(3)
    if user_choice == '1': #Ajout manuel
        id_joueur = ajouter_joueur_manuellement()
        id_equipe = creation_connexion_equipe()
        CURSOR.execute("INSERT INTO equipe_joueur (id_equipe, id_joueur,poste,titre_joueur) VALUES(%s,%s,%s,%s)",(id_joueur,id_equipe,poste(),"Réserviste"))
        CONN.commit()
    elif user_choice == '2': #Ajout par algorithme
        pass
    elif user_choice == '3': #Voir liste des joueurs ajoutés
        pass
    elif user_choice in ['X', 'x']:
        print("Retour au menu de gestion de l'équipe.")

def afficher_joueur_equipe():
    def afficher_titulaires():
        sql = "SELECT * FROM joueur WHERE est_titulaire = 1"
        CURSOR.execute(sql)
        result = CURSOR.fetchall()
        if result:
            headers = ["ID", "Nom", "Prénom", "Vitesse", "Score Technique", "Force", "Endurance", "Blessure", "Titulaire"]
            table = [list(row) for row in result]
            print("Joueurs Titulaires :")
            print(tabulate(table, headers, tablefmt="grid"))
        else:
            print("Aucun joueur titulaire trouvé.")

def gestion_equipe():
    clear_console()
    afficher_txt(MENU_GESTION_EQUIPE)
    user_choice = choix_interface(3)
    if user_choice == '1':#Recruter un joueur
        recruter_joueur()
    elif user_choice == '2':#configuration-mise en place des titulaires, ajout et modification de poste/
        pass
    elif user_choice == '3':#afficher les joueurs insérer dans la BDD
        clear_console()
        afficher_joueurs_disponibles()
        if input("Entrer pour quitter : ") == "" :
            gestion_equipe()
