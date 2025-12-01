from fonction_utilitaire.utilitaire import *
from tabulate import tabulate

def ajouter_joueur_manuellement() ->None: #Fonction d'ajout manuel de joueur
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
    except ValueError or mysql.connector.errors.ProgrammingError:
        print("Il semblerait qu'une erreur s'est produite. Veuillez réessayer.")
        ajouter_joueur_manuellement()


def ajouter_joueur_par_algorithme() ->None: #Fonction d'ajout de joueur par algorithme (Aléatoirement)
    pass

def changer_configuration_equipe() ->None: #Fonction de changement de configuration d'équipe
    pass


def gestion_joueur(): #Fonction principale de gestion des joueurs(main)
    clear_console()
    afficher_txt(MENU_GESTION_JOUEUR)
    user_choice = choix_interface(3)
    if user_choice == '1': #Recrutement de joueur
        clear_console()
        afficher_txt(CHOIX_AJOUT_JOUEUR)
        user_choice = choix_interface(3)
        if user_choice == '1': #Ajout manuel
            ajouter_joueur_manuellement()
        elif user_choice == '2': #Ajout par algorithme
            pass
        elif user_choice == '3': #Voir liste des joueurs ajoutés
            pass
        elif user_choice in ['X', 'x']:
            print("Retour au menu de gestion de l'équipe.")
    elif user_choice == '2': #Changer configuration
        pass
    elif user_choice == '3': #Voir liste des joueurs
        pass
    elif user_choice in ['X', 'x']:
        print("Retour au menu principal.")

gestion_joueur()