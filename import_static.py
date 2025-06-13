# import_static.py
import requests
import sqlite3
import time

DB_PATH = "eau_potable.db"

def fetch_and_populate_static():
    """
    1) Phase 1 : remplir Commune et Reseau via '/communes_udi'
    2) Phase 2 : pour chaque commune, lire TOUS les paramètres dans '/resultats_dis'
                 -> insérer chaque paramètre dans parameter
                 -> utiliser l'objet [0] pour remplir Departement/Distributeur/Commune/Reseau
    """

    # ─── Phase 1 : COMMUNE + RESEAU ───────────────────────────────────────────
    url_communes_udi = "https://hubeau.eaufrance.fr/api/v1/qualite_eau_potable/communes_udi?size=20"
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    page = 1
    while True:
        url = f"{url_communes_udi}&page={page}"
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
        except Exception as e:
            print(f"Erreur page {page} communes_udi : {e}")
            break

        data = resp.json().get("data", [])
        if not data:
            break

        for obj in data:
            code_c = obj.get("code_commune")
            nom_c  = obj.get("nom_commune")
            code_r = obj.get("code_reseau")
            nom_r  = obj.get("nom_reseau")
            nom_q  = obj.get("nom_quartier")
            debut  = obj.get("debut_alim")
            annee  = obj.get("annee")

            if code_c and nom_c:
                cur.execute(
                    "INSERT OR IGNORE INTO Commune (code_commune, nom_commune) VALUES (?, ?)",
                    (code_c, nom_c)
                )

            if code_r:
                cur.execute("""
                    INSERT OR IGNORE INTO Reseau (
                        code_reseau,
                        nom_reseau,
                        nom_quartier,
                        debut_alim,
                        annee,
                        code_commune,
                        nom_uge
                    ) VALUES (?, ?, ?, ?, ?, ?, NULL)
                """, (code_r, nom_r, nom_q, debut, annee, code_c))

        conn.commit()
        print(f"✔ Page {page} '/communes_udi' traitée ({len(data)} lignes).")
        page += 1
        time.sleep(0.05)

    # ─── Phase 2 : PARAMETRE + DEPARTEMENT + DISTRIBUTEUR ─────────────────────
    url_resultats = "https://hubeau.eaufrance.fr/api/v1/qualite_eau_potable/resultats_dis?size=20"
    cur.execute("SELECT code_commune FROM Commune")
    communes = [row[0] for row in cur.fetchall()]

    for code_c in communes:
        url2 = f"{url_resultats}&code_commune={code_c}"
        try:
            resp2 = requests.get(url2, timeout=10)
            resp2.raise_for_status()
        except Exception as e:
            print(f"Erreur '/resultats_dis' pour la commune {code_c} : {e}")
            continue

        data2 = resp2.json().get("data", [])
        if not data2:
            continue

        # ── 2.A) Parcourir TOUS les objets "paramètre" retournés (index 0 à len-1)
        for param_obj in data2:
            code_par       = param_obj.get("code_parametre")
            code_par_se    = param_obj.get("code_parametre_se")
            code_par_cas   = param_obj.get("code_parametre_cas")
            libelle_p      = param_obj.get("libelle_parametre")
            libelle_p_maj  = param_obj.get("libelle_parametre_maj")
            code_type_par  = param_obj.get("code_type_parametre")
            libelle_unite  = param_obj.get("libelle_unite")
            code_unite     = param_obj.get("code_unite")
            limite_qualite = param_obj.get("limite_qualite_parametre")

            if code_par:
                cur.execute("""
                    INSERT OR IGNORE INTO Parametre (
                        code_parametre,
                        code_parametre_se,
                        code_parametre_cas,
                        libelle_parametre,
                        libelle_parametre_maj,
                        code_type_parametre,
                        libelle_unite,
                        code_unite,
                        limite_qualite_parametre
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    code_par,
                    code_par_se,
                    code_par_cas,
                    libelle_p,
                    libelle_p_maj,
                    code_type_par,
                    libelle_unite,
                    code_unite,
                    limite_qualite
                ))

        # ── 2.B) Sur le premier objet (index 0), on récupère aussi
        #       code_departement / nom_departement / nom_uge / nom_distributeur / nom_moa
        premier = data2[0]
        dept     = premier.get("code_departement")
        nomd     = premier.get("nom_departement")
        nom_uge  = premier.get("nom_uge")
        nom_dist = premier.get("nom_distributeur")
        nom_moa  = premier.get("nom_moa")

        if dept and nomd:
            cur.execute(
                "INSERT OR IGNORE INTO Departement (code_departement, nom_departement) VALUES (?, ?)",
                (dept, nomd)
            )
            cur.execute(
                "UPDATE Commune SET code_departement = ?, nom_departement = ? WHERE code_commune = ?",
                (dept, nomd, code_c)
            )

        if nom_uge:
            cur.execute("""
                INSERT OR IGNORE INTO Distributeur (nom_uge, nom_distributeur, nom_moa)
                VALUES (?, ?, ?)
            """, (nom_uge, nom_dist, nom_moa))

            cur.execute("""
                UPDATE Commune
                   SET nom_uge = ?, nom_distributeur = ?, nom_moa = ?
                 WHERE code_commune = ?
            """, (nom_uge, nom_dist, nom_moa, code_c))

            cur.execute(
                "UPDATE Reseau SET nom_uge = ? WHERE code_commune = ?",
                (nom_uge, code_c)
            )

        conn.commit()
        time.sleep(0.05)

    conn.close()
    print("✅ Importation terminée avec succès.")


if __name__ == "__main__":
    fetch_and_populate_static()

