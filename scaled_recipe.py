"""Utilities for scaling recipes to a target energy."""

from copy import deepcopy
from recalculate_nutrients import recalculate_nutrients


def scale_recipe_to_energy(recipe, target_energy_kj):
    """Return a new recipe scaled to target energy plus recalculated nutrients."""

    current_nutrients = recalculate_nutrients(
        recipe
    )  # Get current nutrients of the recipe
    current_energy_kj = current_nutrients.get("energy_kj") or 0

    if current_energy_kj <= 0:
        return deepcopy(recipe), current_nutrients

    scale = target_energy_kj / current_energy_kj

    # Scale each ingredient's portion_g
    scaled_recipe = deepcopy(recipe)
    for ingredient in scaled_recipe.get("ingredients", []):
        portion_g = ingredient.get("portion_g", 0)
        ingredient["portion_g"] = int(round(portion_g * scale))

    scaled_nutrients = recalculate_nutrients(scaled_recipe)
    return scaled_recipe, scaled_nutrients
