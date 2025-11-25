import os
import sqlite3
from config import*
conn = sqlite3.connect(SPORT_MANAGER_DB)
cursor = conn.cursor()

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
