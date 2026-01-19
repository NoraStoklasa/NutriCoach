import sqlite3
from config import RECIPE_DB_PATH

VALID_CATEGORIES = {"breakfast", "lunch", "dinner", "snack"}


def create_recipe_tables():
    with sqlite3.connect(RECIPE_DB_PATH) as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            instructions TEXT,
            image_path TEXT
        )
        """
        )

        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS recipe_ingredients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipe_id INTEGER NOT NULL,
            ingredient_name TEXT NOT NULL,
            portion_g REAL NOT NULL,
            FOREIGN KEY (recipe_id) REFERENCES recipes(id)
        )
        """
        )


def create_recipe(name, category, instructions="", image_path=None):
    if category not in VALID_CATEGORIES:
        raise ValueError("Invalid recipe category")

    with sqlite3.connect(RECIPE_DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO recipes (name, category, instructions, image_path)
            VALUES (?, ?, ?, ?)
            """,
            (name.strip(), category, instructions, image_path),
        )
        return cursor.lastrowid


def add_recipe_ingredient(recipe_id, ingredient_name, portion_g):
    if portion_g <= 0:
        raise ValueError("Ingredient portion must be greater than 0.")

    with sqlite3.connect(RECIPE_DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO recipe_ingredients (recipe_id, ingredient_name, portion_g)
            VALUES (?, ?, ?)
            """,
            (recipe_id, ingredient_name, portion_g),
        )


def update_recipe(recipe_id, name, category, instructions="", image_path=None):
    if category not in VALID_CATEGORIES:
        raise ValueError("Invalid recipe category")

    with sqlite3.connect(RECIPE_DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE recipes
            SET name = ?, category = ?, instructions = ?, image_path = ?
            WHERE id = ?
            """,
            (name.strip(), category, instructions, image_path, recipe_id),
        )


def replace_recipe_ingredients(recipe_id, ingredients):
    with sqlite3.connect(RECIPE_DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM recipe_ingredients WHERE recipe_id = ?",
            (recipe_id,),
        )
        cursor.executemany(
            """
            INSERT INTO recipe_ingredients (recipe_id, ingredient_name, portion_g)
            VALUES (?, ?, ?)
            """,
            [
                (recipe_id, ing["name"], ing["portion_g"])
                for ing in ingredients
                if ing["name"] and ing["portion_g"] > 0
            ],
        )


def load_recipe(recipe_id):
    with sqlite3.connect(RECIPE_DB_PATH) as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT name, category, instructions, image_path
            FROM recipes
            WHERE id = ?
            """,
            (recipe_id,),
        )
        recipe_row = cursor.fetchone()

        if not recipe_row:
            return None

        cursor.execute(
            """
            SELECT ingredient_name, portion_g
            FROM recipe_ingredients
            WHERE recipe_id = ?
            """,
            (recipe_id,),
        )

        ingredients = [
            {"name": name, "portion_g": portion} for name, portion in cursor.fetchall()
        ]

        return {
            "name": recipe_row[0],
            "category": recipe_row[1],
            "instructions": recipe_row[2],
            "image_path": recipe_row[3],
            "ingredients": ingredients,
        }
