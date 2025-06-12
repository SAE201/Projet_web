# create_db.py
import sqlite3

SQL_SCHEMA_FILE = "Base_donnee.sql"
DB_FILE         = "eau_potable.db"

def create_database():
    """Créée (ou recrée) la base SQLite en exécutant le script SQL."""
    with open(SQL_SCHEMA_FILE, "r", encoding="utf-8") as f:
        sql_script = f.read()

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.executescript(sql_script)
    conn.commit()
    conn.close()
    print(f"✔︎ Base de données '{DB_FILE}' créée (ou réinitialisée).")

if __name__ == "__main__":
    create_database()
