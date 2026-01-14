"""Service to synchronize recipe ingredients with the local database and USDA database"""

from ingredients import (
    search_ingredient,
    extract_nutrients,
    extract_portion,
    extract_usda_food_id,
)
from database import (
    insert_ingredient_information,
    extract_ingredient_by_name,
)


def ensure_recipe_ingredients_exist(recipe):
    """Ensure all recipe ingredients exist in the local database by name only"""

    for ingredient in recipe["ingredients"]:
        name = ingredient["name"]

        # Check local database first
        if extract_ingredient_by_name(name):
            print(f"Ingredient '{name}' already exists in database.")
            print("-----")
            continue

        print(f"Ingredient '{name}' not found in database. Skipping.")
        print("-----")
