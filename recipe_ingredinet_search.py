from ingredients import (
    search_ingredient,
    extract_nutrients,
    extract_portion,
    extract_usda_food_id,
)
from recipe import raspberry_cheesecake


ingredient_names = []

for ingredient in raspberry_cheesecake["ingredients"]:
    ingredient_names.append(ingredient["name"])


print(ingredient_names)


for ingredient_name in ingredient_names:
    ingredient = search_ingredient(ingredient_name)
    ingredient_dict_nutrients = extract_nutrients(ingredient)
    ingredient_portion = extract_portion(ingredient)
    ingredient_usda_id = extract_usda_food_id(ingredient)

    print(f"Ingredient: {ingredient_name}")
    print(ingredient_dict_nutrients)
    print(ingredient_portion)
    print(ingredient_usda_id)
    print("-----")
