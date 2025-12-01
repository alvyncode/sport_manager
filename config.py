#Chemains d'accès aux fichiers de configuration
import mysql.connector

MENU = "affichage_et_rendu\menu.txt"
MENU_GESTION_JOUEUR = "affichage_et_rendu\menu_gestion_joueur"
CHOIX_AJOUT_JOUEUR = "affichage_et_rendu\choix_ajout_joueur"

CONN = mysql.connector.connect(
    host= "localhost",
    user= "root",
    password= "",
    database= "sport_manager"
)

CURSOR = CONN.cursor()