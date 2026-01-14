# NutriCoach

NutriCoach is a small Python application designed to help nutritionists **manage ingredients**, **calculate recipe nutrition**, and **scale meals to a target energy value**.

The project focuses on accuracy, flexibility, and simplicity, following realistic professional nutrition workflows.

---

## What NutriCoach can do (v1)

### Ingredient management

- Stores ingredients in a local SQLite database
- Each ingredient contains:
  - reference portion (usually 100 g)
  - energy (kJ)
  - protein, carbohydrates, fat, fibre
- Ingredients can be:
  - fetched automatically from the USDA FoodData Central database
  - added or corrected manually by the nutritionist

This gives the nutritionist full control over data quality.

---

### Recipe nutrition calculation

- Recipes are defined using ingredient names and gram amounts
- The program:
  - looks up ingredients in the database
  - scales nutrients correctly
  - calculates total recipe nutrition
- Results include:
  - total energy (kJ)
  - protein, carbs, fat, fibre

All calculations are based on grams for accuracy.

---

### Recipe scaling by energy

- A recipe can be scaled to a target energy value (kJ)
- All ingredient amounts are adjusted proportionally
- The nutritional balance of the recipe is preserved

This is useful for portion control and meal planning.

---

### Human-friendly units (optional)

- Internally, all calculations use grams
- For display purposes only, some ingredients can be shown in units
  (e.g. eggs, bananas, slices of bread)
- Units are approximate and never affect calculations

This keeps results readable without losing precision.

---

## What NutriCoach does NOT do (by design)

- It does not automatically optimise macros
- It does not make dietary decisions
- It does not replace a nutritionist’s judgement

NutriCoach is a **calculation and data tool**, not an AI nutrition advisor.

---

## Project structure

- `database.py`
  Handles all SQLite database operations

- `ingredients.py`
  Fetches and parses nutrition data from the USDA FoodData Central API

- `ingredient_service.py`
  Ensures recipe ingredients exist in the local database

- `manual_ingredient.py`
  Allows manual addition of ingredients by the nutritionist

- `recalculate_nutrients.py`
  Calculates total recipe nutrition

- `scaled_recipe.py`
  Scales recipes to a target energy value

- `units.py`
  Optional human-friendly unit display (display only)

- `recipe.py`
  Example recipe definitions

- `main.py`
  Example entry point demonstrating the workflow

---

## Typical nutritionist workflow

1. Add ingredients manually or fetch them from USDA
2. Build recipes using ingredient names and grams
3. Calculate total nutrition for the recipe
4. Scale the recipe to a desired energy value
5. Read results in grams (and optional units)

---

## Why this approach

- Uses grams for accuracy
- Allows manual control over ingredient data
- Avoids hidden assumptions
- Keeps logic simple and reliable
- Matches real professional nutrition workflows

---

## Future ideas (not part of v1)

- User interface (web or desktop)
- Ingredient search and edit screen
- Recipe export (PDF)
- Multiple clients / meal plans
- Optional macro warnings or summaries

---

## Status

**NutriCoach v1**
Stable, usable foundation focused on correctness and clarity.
