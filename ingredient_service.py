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


def sync_recipe_ingredients(recipe):
    """Ensure all recipe ingredients exist in the local database if not search USDA and insert them"""

    for ingredient in recipe["ingredients"]:
        name = ingredient["name"]

        # Check local database first
        if extract_ingredient_by_name(name):
            print(f"Ingredient '{name}' already exists in database.")
            print("-----")
            continue

        # Fetch from USDA
        food = search_ingredient(name)
        if not food:
            print(f"Ingredient '{name}' not found in USDA database.")
            print("-----")
            continue

        nutrients = extract_nutrients(food)
        portion = extract_portion(food)
        usda_id = extract_usda_food_id(food)

        insert_ingredient_information(
            name=name,
            usda_food_id=usda_id,
            portion_g=portion,
            energy_kj=nutrients["energy_kj"],
            protein_g=nutrients["protein_g"],
            carbs_g=nutrients["carbs_g"],
            fat_g=nutrients["fat_g"],
            fibre_g=nutrients["fibre_g"],
        )

        print(f"Ingredient '{name}' added to database.")
        print("-----")
