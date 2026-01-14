"""Service to synchronize recipe ingredients with the local database and USDA database"""

from database import extract_ingredient_by_name, insert_ingredient_information
from ingredients import (
    extract_nutrients,
    extract_portion,
    extract_usda_food_id,
    search_ingredient,
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

        food_data = search_ingredient(name)
        if not food_data:
            print(f"Ingredient '{name}' not found in USDA. Skipping.")
            print("-----")
            continue

        nutrients = extract_nutrients(food_data)
        portion_g = extract_portion(food_data)
        usda_food_id = extract_usda_food_id(food_data)

        insert_ingredient_information(
            name,
            usda_food_id,
            portion_g,
            nutrients.get("energy_kj"),
            nutrients.get("protein_g"),
            nutrients.get("carbs_g"),
            nutrients.get("fat_g"),
            nutrients.get("fibre_g"),
        )

        print(f"Ingredient '{name}' added to database.")
        print("-----")
