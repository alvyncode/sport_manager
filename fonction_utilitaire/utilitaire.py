import os
from config import*

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def choix_interface(nbr_options):
    choix = input()
    if choix in ['X', 'x']:
        return choix
    try:
        choix_int = int(choix)
        if choix_int >= 1 and choix_int <= nbr_options:
            return choix
        else:
            print("Choix invalide. Veuillez réessayer.")
            return choix_interface(nbr_options)
    except ValueError  :
        print("Entrée invalide. Veuillez réessayer.")
        return choix_interface(nbr_options)
    
def afficher_txt(fichier_texte):
    with open(fichier_texte, "r", encoding="utf-8") as fichier:
        affichage = fichier.read()
    print(affichage)

def poste()->str:
    afficher_txt("affichage_et_rendu/selection_poste")
    poste = input("Poste :")
    if poste == '1':
        return "Gardien"
    elif poste == '2':
        return "Défenseur"
    elif poste == '3':
        return "Milieu de terrain"
    elif poste == '4':
        return "Attaquant"

def titre()->str:
    afficher_txt("affichage_et_rendu/selection_titre")
    titre = input("Titre :")
    if titre == '1':
        return "Titulaire"
    elif titre == '2':
        return "Réserviste"

def creation_connexion_equipe()->int:#retourne l'id de l'equipe pour remplir la table de liaison equipe_joueur
    nom_equipe = input("Créer une équipe si vous en avez pas.\nDans le cas contraire, nous nous chargerons de la connexion :\n")
    CURSOR.execute("SELECT id_equipe FROM equipe WHERE nom_equipe = %s",(nom_equipe,))
    result = CURSOR.fetchone()
    if result is not None :
        return result[0]
    else:
        CURSOR.execute("INSERT INTO equipe (nom_equipe, score_equipe) VALUES (%s, %s)",(nom_equipe,0))
        CONN.commit()
        return int(CURSOR.lastrowid)
