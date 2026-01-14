from database import create_table
from recipe import raspberry_cheesecake, beef_mince_in_tomatoe_sauce_with_pasta
from ingredient_service import ensure_recipe_ingredients_exist
from recalculate_nutrients import recalculate_nutrients
from scaled_recipe import scale_recipe_to_energy, adjust_recipe_macros


def main():

    # 1. Initialize the database
    create_table()

    # 2. Check if ingredients from a recipe exist in the database, if not fetch from USDA and insert
    ensure_recipe_ingredients_exist(raspberry_cheesecake)
    ensure_recipe_ingredients_exist(beef_mince_in_tomatoe_sauce_with_pasta)

    # 3. Recalculate and print total nutrients for the recipes
    raspberry_cheesecake_recalculated = recalculate_nutrients(raspberry_cheesecake)
    beef_mince_in_tomatoe_sauce_with_pasta_recalculated = recalculate_nutrients(
        beef_mince_in_tomatoe_sauce_with_pasta
    )

    # 4. Print results
    # print("Raspberry Cheesecake Nutrients Recalculated:")
    # print(raspberry_cheesecake_recalculated)
    # print("-----")
    # print("Beef Mince in Tomatoe Sauce with Pasta Nutrients Recalculated:")
    # print(beef_mince_in_tomatoe_sauce_with_pasta_recalculated)
    # print("-----")

    target_energy_kj = 2800
    scaled_pasta, scaled_pasta_nutrients = scale_recipe_to_energy(
        beef_mince_in_tomatoe_sauce_with_pasta, target_energy_kj
    )
    print(f"Beef Mince in Tomatoe Sauce with Pasta Scaled to {target_energy_kj} kJ:")
    print(scaled_pasta)
    print("Scaled nutrients:")
    print(scaled_pasta_nutrients)
    print("-----")

    macro_targets = {
        "protein_g": 50,
        "carbs_g": 50,
        "fibre_min_g": 13,
    }
    adjusted_pasta, adjusted_nutrients, macro_diffs = adjust_recipe_macros(
        scaled_pasta, macro_targets
    )
    print("Adjusted macros (soft targets):")
    print(adjusted_pasta)
    print("Adjusted nutrients:")
    print(adjusted_nutrients)
    print("Macro differences vs targets:")
    rounded_macro_diffs = {
        key: round(value, 2) for key, value in macro_diffs.items()
    }
    print(rounded_macro_diffs)


if __name__ == "__main__":
    main()
