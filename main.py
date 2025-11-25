from fonction_utilitaire.utilitaire import *
from fonction_utilitaire.utilitaire import afficher_txt

def main():
    clear_console()
    afficher_txt(MENU)
    user_choice = choix_interface(3)
    if user_choice == '1':
        print("Gérer joueur sélectionné.")
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


if __name__ == "__main__":
    print("This script is being run directly.")