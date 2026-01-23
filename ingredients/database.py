"""Database interaction functions for ingredients"""

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
    """Insert or update ingredient information by USDA ID"""

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO ingredients (
                name,
                usda_food_id,
                portion_g,
                energy_kj,
                protein_g,
                carbs_g,
                fat_g,
                fibre_g
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(usda_food_id) DO UPDATE SET
                name = excluded.name,
                portion_g = excluded.portion_g,
                energy_kj = excluded.energy_kj,
                protein_g = excluded.protein_g,
                carbs_g = excluded.carbs_g,
                fat_g = excluded.fat_g,
                fibre_g = excluded.fibre_g
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


def extract_ingredient_by_name(name):
    """Extract ingredient information by name from the database"""

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM ingredients WHERE name = ?",
            (name,),
        )
        return cursor.fetchone()  # Returns a tuple or None if not found


def get_all_ingredient_names():
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("SELECT name FROM ingredients ORDER BY name")
        return [row[0] for row in cur.fetchall()]


def search_ingredient_names(query, limit=20):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT name
            FROM ingredients
            WHERE name LIKE ?
            ORDER BY name
            LIMIT ?
            """,
            (f"%{query}%", limit),
        )
        return [row[0] for row in cur.fetchall()]
