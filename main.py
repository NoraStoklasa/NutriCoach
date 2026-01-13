from ingredients import (
    search_ingredient,
    extract_nutrients,
    extract_portion,
    extract_usda_food_id,
)
from database import create_table, insert_ingredient_information
from recipe import raspberry_cheesecake


def main():
    create_table()

    # ingredient = "Belvita Chocolate Breakfast Biscuits"

    # result = search_ingredient(ingredient)

    # dict_nutrient = extract_nutrients(result)
    # portion = extract_portion(result)
    # usda_food_id = extract_usda_food_id(result)

    # insert_ingredient_information(
    #     name=ingredient,
    #     usda_food_id=usda_food_id,
    #     portion_g=portion,
    #     energy_kj=dict_nutrient["energy_kj"],
    #     protein_g=dict_nutrient["protein_g"],
    #     carbs_g=dict_nutrient["carbs_g"],
    #     fat_g=dict_nutrient["fat_g"],
    #     fibre_g=dict_nutrient["fibre_g"],
    # )

    # print(dict_nutrient)
    # print(portion)

    ingredient_names = []

    for ingredient in raspberry_cheesecake["ingredients"]:
        ingredient_names.append(ingredient["name"])

    print(ingredient_names)

    for name in ingredient_names:
        food = search_ingredient(name)
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

        print(f"Ingredient: {name}")
        print(nutrients)
        print(portion)
        print(usda_id)
        print("-----")


if __name__ == "__main__":
    main()
