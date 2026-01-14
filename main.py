from database import create_table
from recipe import (
    raspberry_cheesecake,
    beef_mince_in_tomatoe_sauce_with_pasta,
    egg_spread,
)
from ingredient_service import ensure_recipe_ingredients_exist
from recalculate_nutrients import recalculate_nutrients
from scaled_recipe import scale_recipe_to_energy
from units import format_portion
from manual_ingredient import add_ingredient_manually


def main():

    # 1. Initialize the database
    create_table()

    # 2. Check if ingredients from a recipe exist in the database, if not fetch from USDA and insert
    ensure_recipe_ingredients_exist(egg_spread)

    # 3. Recalculate and print total nutrients for the recipes
    egg_spread_recalculated = recalculate_nutrients(egg_spread)

    # 4. Print results
    print("Egg Spread Nutrients Recalculated:")
    print(egg_spread_recalculated)
    print("-----")

    # 5. Scale recipe to target energy
    target_energy_kj = 2000
    scaled_egg_spread, scaled_egg_spread_nutrients = scale_recipe_to_energy(
        egg_spread, target_energy_kj
    )
    print(f"Egg Spread Scaled to {target_energy_kj} kJ:")
    print(scaled_egg_spread)
    print("Scaled nutrients:")
    print(scaled_egg_spread_nutrients)
    print("-----")

    print("Ingredients:")
    for ingredient in scaled_egg_spread["ingredients"]:
        name = ingredient["name"]
        grams = ingredient["portion_g"]
        print(f"- {name}: {format_portion(name, grams)}")


add_ingredient_manually(
    name="Rolled Oats",
    portion_g=100,
    energy_kj=1586,
    protein_g=13.1,
    carbs_g=57.6,
    fat_g=6.5,
    fibre_g=100,
)

if __name__ == "__main__":
    main()
