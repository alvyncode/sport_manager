#Chemains d'accès aux fichiers de configuration
import mysql.connector

MENU = "affichage_et_rendu\menu.txt"
CHOIX_AJOUT_JOUEUR = "affichage_et_rendu\choix_ajout_joueur"
MENU_GESTION_EQUIPE = "affichage_et_rendu\menu_gestion_equipe"

CONN = mysql.connector.connect(
    host= "localhost",
    user= "root",
    password= "",
    database= "sport_manager"
)

CURSOR = CONN.cursor()