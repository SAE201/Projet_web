import sqlite3
import requests
import time

DB_FILE = "eau_potable.db"

def update_parameters(cursor):
    print(" Mise à jour des paramètres...")
    url = "https://hubeau.eaufrance.fr/api/v1/qualite_eau_potable/parametres?size=500"
    data = requests.get(url).json().get("data", [])

    for param in data:
        cursor.execute('''
            INSERT OR REPLACE INTO Parametre (
                code_parametre, code_parametre_se, code_parametre_cas,
                libelle_parametre, libelle_parametre_maj, code_type_parametre,
                libelle_unite, code_unite, limite_qualite_parametre
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            param.get("code_parametre"),
            param.get("code_parametre_se"),
            param.get("code_parametre_cas"),
            param.get("libelle_parametre"),
            param.get("libelle_parametre_maj"),
            param.get("code_type_parametre"),
            param.get("libelle_unite"),
            param.get("code_unite"),
            param.get("limite_qualite_parametre")
        ))
    print(f"{len(data)} paramètres mis à jour.")

def update_communes_reseaux(cursor):
    print(" Mise à jour des communes et réseaux...")
    url = "https://hubeau.eaufrance.fr/api/v1/qualite_eau_potable/communes_udi?size=100"
    page = 1
    count_commune, count_reseau = 0, 0

    while True:
        response = requests.get(f"{url}&page={page}")
        if response.status_code != 200:
            break

        data = response.json().get("data", [])
        if not data:
            break

        for row in data:
            code_commune = row.get("code_commune")
            nom_commune = row.get("nom_commune")
            code_reseau = row.get("code_reseau")
            nom_reseau = row.get("nom_reseau")
            nom_quartier = row.get("nom_quartier")
            debut_alim = row.get("debut_alim")
            annee = row.get("annee")

            if code_commune:
                cursor.execute("""
                    INSERT OR REPLACE INTO Commune (code_commune, nom_commune)
                    VALUES (?, ?)
                """, (code_commune, nom_commune))
                count_commune += 1

            if code_reseau:
                cursor.execute("""
                    INSERT OR REPLACE INTO Reseau (
                        code_reseau, nom_reseau, nom_quartier,
                        debut_alim, annee, code_commune, nom_uge
                    ) VALUES (?, ?, ?, ?, ?, ?, (
                        SELECT nom_uge FROM Commune WHERE code_commune = ?
                    ))
                """, (code_reseau, nom_reseau, nom_quartier, debut_alim, annee, code_commune, code_commune))
                count_reseau += 1

        page += 1
        time.sleep(0.1)

    print(f" {count_commune} communes mises à jour.")
    print(f" {count_reseau} réseaux mis à jour.")

def main():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    update_parameters(cur)
    update_communes_reseaux(cur)

    conn.commit()
    conn.close()
    print(" Maintenance terminée.")

if __name__ == "__main__":
    main()
