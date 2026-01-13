import sqlite3
from config import DB_PATH


def create_table():
    """Create the ingredients table in the database if it doesn't exist"""
    with sqlite3.connect(DB_PATH) as conn:
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


def insert_ingredient_information(
    name, usda_food_id, portion_g, energy_kj, protein_g, carbs_g, fat_g, fibre_g
):
    """Insert or update ingredient information in the database"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
    INSERT OR REPLACE INTO ingredients (name, usda_food_id, portion_g, energy_kj, protein_g, carbs_g, fat_g, fibre_g)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """,
            (
                name,
                usda_food_id,
                portion_g,
                energy_kj,
                protein_g,
                carbs_g,
                fat_g,
                fibre_g,
            ),
        )
