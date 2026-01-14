from database import create_table
from recipe import raspberry_cheesecake, beef_mince_in_tomatoe_sauce_with_pasta
from ingredient_service import ensure_recipe_ingredients_exist
from recalculate_nutrients import recalculate_nutrients
from scaled_recipe import scale_recipe_to_energy


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

    target_energy_kj = 3000
    scaled_pasta = scale_recipe_to_energy(
        beef_mince_in_tomatoe_sauce_with_pasta, target_energy_kj
    )
    print(f"Beef Mince in Tomatoe Sauce with Pasta Scaled to {target_energy_kj} kJ:")
    print(scaled_pasta)
    print("-----")


if __name__ == "__main__":
    main()
