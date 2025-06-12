# test_db.py
import sqlite3

DB_FILE = "eau_potable.db"

def main():
    conn = sqlite3.connect(DB_FILE)
    cur  = conn.cursor()

    print("── 5 premiers DEPARTEMENTS ───────────────────")
    cur.execute("SELECT code_departement, nom_departement FROM Departement LIMIT 5;")
    for row in cur.fetchall():
        print(row)

    print("\n── 5 premières COMMUNES ──────────────────────")
    cur.execute("""
        SELECT 
            code_commune, 
            nom_commune, 
            code_departement, 
            nom_departement,
            nom_uge,
            nom_distributeur,
            nom_moa
          FROM Commune
         LIMIT 5;
    """)
    for row in cur.fetchall():
        print(row)

    print("\n── 5 premiers DISTRIBUTEURS (UGE / MOA) ──────")
    cur.execute("""
        SELECT nom_uge, nom_distributeur, nom_moa 
          FROM Distributeur
         LIMIT 5;
    """)
    for row in cur.fetchall():
        print(row)

    print("\n── 5 premiers RÉSEAUX (UDI) ──────────────────")
    cur.execute("""
        SELECT 
            code_reseau, 
            nom_reseau, 
            nom_quartier,
            debut_alim,
            annee,
            code_commune,
            nom_uge
          FROM Reseau
         LIMIT 5;
    """)
    for row in cur.fetchall():
        print(row)

    print("\n── 5 premiers PARAMÈTRES (SANDRE) ────────────")
    cur.execute("""
        SELECT 
            code_parametre,
            code_parametre_se,
            code_parametre_cas,
            libelle_parametre,
            libelle_parametre_maj,
            code_type_parametre,
            libelle_unite,
            code_unite,
            limite_qualite_parametre
          FROM Parametre
         LIMIT 5;
    """)
    rows = cur.fetchall()
    if not rows:
        print("(aucune ligne : la table Parametre est vide)")
    else:
        for row in rows:
            print(row)

    conn.close()

if __name__ == "__main__":
    main()
