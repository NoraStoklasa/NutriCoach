"""Recalculate nutrients for recipes based on their ingredients"""

from database import extract_ingredient_by_name


def recalculate_nutrients(recipe):
    """Recalculate total nutrients for a recipe based on its ingredients"""

    total_nutrients = {
        "energy_kj": 0,
        "protein_g": 0,
        "carbs_g": 0,
        "fat_g": 0,
        "fibre_g": 0,
    }

    for ingredient in recipe["ingredients"]:
        name = ingredient["name"]
        portion_g = ingredient.get("portion_g", 0)

        # Fetch ingredient info from the database
        ingredient_info = extract_ingredient_by_name(name)
        if not ingredient_info:
            print(f"Ingredient '{name}' not found in database. Skipping.")
            continue

        portion__g = ingredient_info[3]
        energy_kj = ingredient_info[4]
        protein_g = ingredient_info[5]
        carbs_g = ingredient_info[6]
        fat_g = ingredient_info[7]
        fibre_g = ingredient_info[8]

        # Calculate scaling factor
        if portion__g:
            scale = portion_g / portion__g
        else:
            scale = 0

        # Update total nutrients
        total_nutrients["energy_kj"] += (energy_kj or 0) * scale
        total_nutrients["protein_g"] += (protein_g or 0) * scale
        total_nutrients["carbs_g"] += (carbs_g or 0) * scale
        total_nutrients["fat_g"] += (fat_g or 0) * scale
        total_nutrients["fibre_g"] += (fibre_g or 0) * scale

    return {
        "energy_kj": int(round(total_nutrients["energy_kj"])),
        "protein_g": round(total_nutrients["protein_g"], 2),
        "carbs_g": round(total_nutrients["carbs_g"], 2),
        "fat_g": round(total_nutrients["fat_g"], 2),
        "fibre_g": round(total_nutrients["fibre_g"], 2),
    }
