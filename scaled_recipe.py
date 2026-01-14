"""Utilities for scaling recipes to a target energy."""

from copy import deepcopy

from recalculate_nutrients import recalculate_nutrients


def scale_recipe_to_energy(recipe, target_energy_kj):
    """Return a new recipe with ingredient grams scaled to target energy."""

    current_nutrients = recalculate_nutrients(recipe)
    current_energy_kj = current_nutrients.get("energy_kj") or 0

    if current_energy_kj <= 0:
        return deepcopy(recipe)

    scale = target_energy_kj / current_energy_kj

    scaled_recipe = deepcopy(recipe)
    for ingredient in scaled_recipe.get("ingredients", []):
        portion_g = ingredient.get("portion_g", 0)
        ingredient["portion_g"] = int(round(portion_g * scale))

    return scaled_recipe
