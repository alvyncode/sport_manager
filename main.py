from fonction_utilitaire.utilitaire import*
from fonction_utilitaire.utilitaire import afficher_txt

def main():
    clear_console()
    nom, prenom, equipe = input("Votre nom :"), input("Votre prénom :"), input("Nom de votre équipe : ")
    CURSOR.execute("INSERT INTO coatch (nom_coatch, prenom_coatch) VALUES (%s, %s)", (nom, prenom))
    CURSOR.execute("INSERT INTO equipe (nom_equipe, id_coatch) VALUES (%s, LAST_INSERT_ID())", (equipe,))
    CONN.commit()
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