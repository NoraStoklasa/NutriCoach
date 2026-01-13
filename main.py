from database import create_table, extract_ingredient_by_name
from recipe import raspberry_cheesecake, beef_mince_in_tomatoe_sauce_with_pasta
from ingredient_service import sync_recipe_ingredients
from ingredients import search_ingredient


def main():
    create_table()
    # sync_recipe_ingredients(raspberry_cheesecake)
    sync_recipe_ingredients(beef_mince_in_tomatoe_sauce_with_pasta)
    # print(extract_ingredient_by_name("Chia Seeds Dried"))
    # print(search_ingredient("Tomato Passata"))


if __name__ == "__main__":
    main()
