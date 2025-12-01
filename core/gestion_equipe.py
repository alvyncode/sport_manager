from config import*
from fonction_utilitaire.utilitaire import *

def creation_equipe():
    nom_equipe = input("Entrez le nom de votre équipe : ")
    clear_console()
    sql = "INSERT INTO equipe (nom_equipe) VALUES (%s)"
    val = (nom_equipe,)
    CURSOR.execute(sql, val)
    CONN.commit()
    i = 0
    while i <=11:
        input("Selectioner vos joueurs pour composer votre équipe. Appuyez sur Entrée pour continuer...")