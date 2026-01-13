from ingredients import (
    search_ingredient,
    extract_nutrients,
    extract_portion,
    extract_usda_food_id,
)
from database import create_table, insert_ingredient_information


def main():
    create_table()

    ingredient = "Belvita Chocolate Breakfast Biscuits"

    result = search_ingredient(ingredient)

    dict_nutrient = extract_nutrients(result)
    portion = extract_portion(result)
    usda_food_id = extract_usda_food_id(result)

    insert_ingredient_information(
        name=ingredient,
        usda_food_id=usda_food_id,
        portion_g=portion,
        energy_kj=dict_nutrient["energy_kj"],
        protein_g=dict_nutrient["protein_g"],
        carbs_g=dict_nutrient["carbs_g"],
        fat_g=dict_nutrient["fat_g"],
        fibre_g=dict_nutrient["fibre_g"],
    )

    print(dict_nutrient)
    print(portion)


if __name__ == "__main__":
    main()
