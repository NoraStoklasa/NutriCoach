import sqlite3

from config import RECIPE_DB_PATH


def parse_float(value, default=0.0):
    """Convert a value to float, returning default for empty/invalid input."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def group_recipes_by_category(recipes, get_category, get_name):
    """Group recipes into categories and sort each category by name."""
    grouped = {
        "breakfast": [],
        "lunch": [],
        "dinner": [],
        "snack": [],
    }
    for recipe in recipes:
        grouped.setdefault(get_category(recipe), []).append(recipe)
    for items in grouped.values():
        items.sort(key=lambda item: get_name(item).lower())
    return grouped


def fetch_recipes_by_category():
    """Fetch recipes from the DB and return them grouped by category."""
    with sqlite3.connect(RECIPE_DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT id, name, category
            FROM recipes
            ORDER BY category, name
        """
        )
        recipes = cur.fetchall()
    return group_recipes_by_category(recipes, lambda r: r[2], lambda r: r[1])


def targets_by_category(form):
    """Read target energy values (kJ) for each category from a form."""
    return {
        "breakfast": parse_float(form.get("target_kj_breakfast")),
        "lunch": parse_float(form.get("target_kj_lunch")),
        "dinner": parse_float(form.get("target_kj_dinner")),
        "snack": parse_float(form.get("target_kj_snack")),
    }


def ingredients_from_form(form, rid):
    """Build ingredient dicts for a recipe ID from a submitted form."""
    names = form.getlist(f"ingredient_name_{rid}")
    portions = form.getlist(f"portion_g_{rid}")
    ingredients = []
    for name, portion_value in zip(names, portions):
        portion = parse_float(portion_value, default=None)
        if portion is None:
            continue
        ingredients.append({"name": name, "portion_g": portion})
    return ingredients
