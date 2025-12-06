from fonction_utilitaire.utilitaire import*
from core.gestion_equipe_main import*
def main():
    clear_console()
    afficher_txt(MENU)
    user_choice = choix_interface(3)
    if user_choice == '1':
        gestion_equipe()
        # Appeler la fonction pour gérer le joueur
    elif user_choice == '2':
        print("Jouer match sélectionné.")
        # Appeler la fonction pour jouer un match
    elif user_choice == '3':
        print("Historique des matchs sélectionné.")
        # Appeler la fonction pour afficher l'historique des matchs
    elif user_choice in ['X', 'x']:
        print("Quitter le programme.")
main()

