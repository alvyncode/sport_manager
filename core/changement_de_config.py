from tabulate import tabulate
from config import*
from fonction_utilitaire.utilitaire import*

def afficher_config_actuelle():
    nom_equipe = input("Quelle est le nom de votre equipe ?")
    CURSOR.execute("SELECT id_equipe FROM equipe WHERE nom_equipe = %s",(nom_equipe,))
    id_equipe = CURSOR.fetchone()[0]
    CURSOR.execute("""
    SELECT ej.id_joueur,j.nom_joueur,prenom_joueur,ej.poste, ej.titre_joueur 
    FROM equipe_joueur ej 
    INNER JOIN joueur j ON ej.id_joueur = j.id_joueur
    WHERE ej.id_equipe = %s""",(id_equipe,))
    result = CURSOR.fetchall()
    if result:
        headers = ["ID", "Nom", "Prénom","Poste","Titre"]
        table = [list(row) for row in result]
        print("Joueurs Disponibles :")
        print(tabulate(table, headers, tablefmt="grid"))
    else:
        print("Aucun joueur disponible trouvé.")

def changer_configuration():
    afficher_config_actuelle()
    id_joueur = input("De quelle joueur souhaitez vous changer le poste et le titre ?")
    clear_console()
    posted = poste()
    clear_console()
    titred = titre()
    CURSOR.execute("SELECT id_equipe FROM equipe_joueur WHERE id_joueur = %s",(id_joueur,))
    equipe = CURSOR.fetchone()[0]
    CURSOR.execute("""SELECT COUNT(*)
                   FROM equipe_joueur
                   WHERE titre = "Titulaire" AND id_equipe =%s
                   """,(equipe,))
    total_titulaire = CURSOR.fetchone()[0]

    while total_titulaire <= 11: 
        CURSOR.execute("""
    UPDATE equipe_joueur
    SET titre_joueur =%s, poste =%s
    WHERE id_joueur = %s """,(titred,posted,id_joueur,))
        CONN.commit()
    else:
        print("Vous avez atteint le quota de titulaires")

