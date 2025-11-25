from fonction_utilitaire.utilitaire import *


def gestion_joueur():
    clear_console()
    afficher_txt(MENU_GESTION_JOUEUR)
    user_choice = choix_interface(3)
    if user_choice == '1':
        print("Ajouter un joueur sélectionné.")
        # Logique d'ajout de joueur ici
    elif user_choice == '2':
        clear_console()
        afficher_txt(CHOIX_AJOUT_JOUEUR)
        # Logique de modification de joueur ici
    elif user_choice == '3':
        print("Supprimer un joueur sélectionné.")
        # Logique de suppression de joueur ici
    elif user_choice in ['X', 'x']:
        print("Retour au menu principal.")
    # Logique de gestion des joueurs ici
gestion_joueur()
