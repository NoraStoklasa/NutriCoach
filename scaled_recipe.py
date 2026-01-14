"""Utilities for scaling recipes to a target energy."""

from copy import deepcopy

from recalculate_nutrients import recalculate_nutrients

PROTEIN_RICH = [
    "Greek yoghurt",
    "YoPRO Danone High Protein Yoghurt Vanilla",
    "Ricotta cheese",
    "Ricotta cheese light",
    "Beef Mince 5% Fat",
    "Parmesan Cheese Grated",
]
FAT_RICH = [
    "Olive oil",
    "Olive Oil",
    "Butter",
    "Parmesan Cheese Grated",
    "Ricotta cheese light",
]
FIBRE_RICH = [
    "Chia seeds",
    "Chia Seeds Dried",
    "Raspberries",
    "Raspberries Frozen",
    "Zucchini Raw",
    "Brown Onion Raw",
]
CARB_RICH = [
    "Spaghetti uncooked",
    "Tomato Passata",
    "Belvita Chocolate Breakfast Biscuits",
]


def _normalize_name(name):
    return str(name or "").strip().lower()


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


def adjust_recipe_macros(recipe, macro_targets, max_iterations=3):
    """Gently adjust ingredient grams toward optional macro targets.

    Energy is assumed to be set already and is not rescaled here. Protein and
    carbs are optional soft targets when provided in macro_targets. Fibre is
    treated as a minimum threshold via fibre_min_g. Fat is never a direct
    target and is only affected indirectly by ingredient changes.
    """

    macro_groups = {
        "protein_g": {_normalize_name(name) for name in PROTEIN_RICH},
        "fibre_g": {_normalize_name(name) for name in FIBRE_RICH},
        "carbs_g": {_normalize_name(name) for name in CARB_RICH},
    }

    adjusted_recipe = deepcopy(recipe)
    current_nutrients = recalculate_nutrients(adjusted_recipe)

    for _ in range(max_iterations):
        macro_diffs = {}
        for macro in ("protein_g", "carbs_g"):
            if macro in macro_targets:
                macro_diffs[macro] = (
                    macro_targets.get(macro, 0) - current_nutrients.get(macro, 0)
                )

        fibre_min_g = macro_targets.get("fibre_min_g")
        if fibre_min_g is not None:
            fibre_gap = fibre_min_g - current_nutrients.get("fibre_g", 0)
            if fibre_gap > 0:
                macro_diffs["fibre_g"] = fibre_gap
        if not macro_diffs:
            break

        target_macro = max(macro_diffs, key=lambda name: abs(macro_diffs[name]))
        ingredient_names = macro_groups.get(target_macro)
        if not ingredient_names:
            break

        increase = macro_diffs[target_macro] > 0
        multiplier = 1.05 if increase else 0.95

        # Nudge only the ingredients tied to the macro being adjusted.
        adjusted_any = False
        for ingredient in adjusted_recipe.get("ingredients", []):
            if _normalize_name(ingredient.get("name")) in ingredient_names:
                portion_g = ingredient.get("portion_g", 0)
                ingredient["portion_g"] = max(0, int(round(portion_g * multiplier)))
                adjusted_any = True

        if not adjusted_any:
            break

        current_nutrients = recalculate_nutrients(adjusted_recipe)

    final_diffs = {
        macro: (macro_targets.get(macro, 0) - current_nutrients.get(macro, 0))
        for macro in ("protein_g", "carbs_g")
        if macro in macro_targets
    }
    fibre_min_g = macro_targets.get("fibre_min_g")
    if fibre_min_g is not None:
        final_diffs["fibre_g"] = fibre_min_g - current_nutrients.get("fibre_g", 0)
    return adjusted_recipe, current_nutrients, final_diffs
