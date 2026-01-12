import sqlite3

DB_PATH = "nutrichoach.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn


def create_tables():
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS ingredients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            usda_food_id INTEGER UNIQUE,
            portion_g REAL,
            energy_kj REAL,
            protein_g REAL,
            carbs_g REAL,
            fat_g REAL,
            fibre_g REAL
        )
    """
    )

    conn.commit()
    conn.close()
