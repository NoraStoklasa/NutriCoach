# NutriCoach

NutriCoach is a small Python project that keeps nutrient data for ingredients
in a local SQLite database and uses it to total up recipe nutrients. It can
also scale ingredient grams so a recipe hits a target energy value (kJ).

## What this project does

- Stores ingredients in a local database (`nutrichoach.db`).
- Calculates recipe totals by combining ingredient nutrients.
- Optionally scales a recipe to reach a target energy value.

## How it works

- A recipe lists ingredient names and grams (`portion_g`).
- Each ingredient in the database stores nutrients per 100g (or per serving).
- Recipe totals are calculated by scaling each ingredient’s nutrients by its grams.
- If you set a target energy, ingredient grams are scaled by one factor.

## Project files

- `main.py`

  - Use this file if you want a quick end-to-end run.
  - `main()` runs a small demo: checks the database, recalculates totals,
    and shows scaling a recipe to a target energy.

- `recipe.py`

  - Acts like a small test input for the demo.
  - Example recipe data (ingredient names and `portion_g` values).

- `database.py`

  - This is the only file that talks directly to SQLite.
  - `create_table()` creates the `ingredients` table if it does not exist.
  - `insert_ingredient_information(...)` inserts or updates one ingredient row.
  - `extract_ingredient_by_name(name)` fetches an ingredient by name.

- `ingredients.py`

  - Useful if you want to expand the database from USDA data.
  - `search_ingredient(name)` searches USDA FoodData Central.
  - `extract_nutrients(...)` and helpers parse nutrient data.
  - If energy (kJ) is missing, it is estimated from macros:
    `protein*17 + carbs*17 + fat*37 + fibre*8`.

- `ingredient_service.py`

  - Keeps recipe checks in one place so `main.py` stays simple.
  - `ensure_recipe_ingredients_exist(recipe)` checks each recipe ingredient
    exists in the local DB. It does not auto-fetch from USDA.

- `recalculate_nutrients.py`

  - Think of this as the "calculator" for recipe totals.
  - `recalculate_nutrients(recipe)` totals nutrients and rounds energy to a
    whole number and other nutrients to two decimals.

- `scaled_recipe.py`
  - This is used when you want a recipe to hit a specific energy target.
  - `scale_recipe_to_energy(recipe, target_energy_kj)` returns a new recipe
    with grams scaled to reach the target energy.

## Key calculations

- Scale factor for an ingredient:
  `portion_g / portion_g_in_database`
- Energy estimate (kJ) when missing:
  `protein_g*17 + carbs_g*17 + fat_g*37 + fibre_g*8`
- Target scaling for a recipe:
  `scale = target_energy_kj / current_energy_kj`
