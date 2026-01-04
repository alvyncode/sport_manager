from config import CURSOR, CONN
import random

# Liste de noms et prénoms français pour génération aléatoire
NOMS = [
    "Dupont", "Martin", "Bernard", "Dubois", "Thomas",
    "Robert", "Richard", "Petit", "Durand", "Leroy",
    "Moreau", "Simon", "Laurent", "Lefebvre", "Michel",
    "Garcia", "David", "Bertrand", "Roux", "Vincent",
    "Fournier", "Morel", "Girard", "Andre", "Lefevre"
]

PRENOMS = [
    "Lucas", "Hugo", "Nathan", "Louis", "Arthur",
    "Gabriel", "Jules", "Raphael", "Tom", "Leo",
    "Adam", "Mathis", "Paul", "Victor", "Antoine",
    "Maxime", "Alexandre", "Pierre", "Thomas", "Nicolas",
    "Baptiste", "Julien", "Kevin", "Romain", "Florian"
]

def initialiser_table_noms_prenoms():
    """Remplit la table nom_prenom_r avec des noms et prénoms prédéfinis"""
    try:
        print("Début de l'initialisation...")
        # Vider la table d'abord (optionnel)
        CURSOR.execute("DELETE FROM nom_prenom_r")
        print("Table vidée.")
        
        # Insérer tous les noms et prénoms
        sql = "INSERT INTO nom_prenom_r (nom, prenom) VALUES (%s, %s)"
        compteur = 0
        for nom in NOMS:
            for prenom in PRENOMS:
                CURSOR.execute(sql, (nom, prenom))
                compteur += 1
        
        CONN.commit()
        print(f"✓ {compteur} combinaisons nom/prénom ajoutées avec succès!")
    except Exception as e:
        print(f"✗ Erreur lors de l'initialisation : {e}")
        import traceback
        traceback.print_exc()
        CONN.rollback()

if __name__ == "__main__":
    initialiser_table_noms_prenoms()