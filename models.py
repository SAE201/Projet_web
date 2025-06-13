# models.py
import sqlite3

DB_PATH = "data/eau_potable.db"

def get_connection():
    """Retourne une connexion SQLite à la base de données locale."""
    return sqlite3.connect(DB_PATH)

def get_all_departements():
    """Liste tous les départements disponibles."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT code_departement, nom_departement FROM Departement ORDER BY nom_departement;")
    rows = cur.fetchall()
    conn.close()
    return [{"code": row[0], "nom": row[1]} for row in rows]

def get_communes_by_dept(code_dept):
    """Retourne les communes d’un département donné."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT code_commune, nom_commune 
        FROM Commune 
        WHERE code_departement = ? 
        ORDER BY nom_commune;
    """, (code_dept,))
    rows = cur.fetchall()
    conn.close()
    return [{"code": row[0], "nom": row[1]} for row in rows]

def get_reseaux_by_commune(code_commune):
    """Retourne les réseaux associés à une commune."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT code_reseau, nom_reseau 
        FROM Reseau 
        WHERE code_commune = ? 
        ORDER BY nom_reseau;
    """, (code_commune,))
    rows = cur.fetchall()
    conn.close()
    return [{"code": row[0], "nom": row[1]} for row in rows]

def get_infos_reseau(code_reseau):
    """Retourne les informations générales d’un réseau."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            R.nom_reseau,
            R.nom_quartier,
            R.debut_alim,
            R.annee,
            D.nom_distributeur,
            D.nom_moa
        FROM Reseau R
        LEFT JOIN Distributeur D ON R.nom_uge = D.nom_uge
        WHERE R.code_reseau = ?;
    """, (code_reseau,))
    row = cur.fetchone()
    conn.close()
    if row:
        return {
            "nom_reseau": row[0],
            "quartier": row[1],
            "debut_alim": row[2],
            "annee": row[3],
            "distributeur": row[4],
            "moa": row[5]
        }
    return None
