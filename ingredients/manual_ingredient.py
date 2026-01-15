from .database import insert_ingredient_information


def add_ingredient_manually(
    name,
    portion_g,
    energy_kj,
    protein_g,
    carbs_g,
    fat_g,
    fibre_g,
):
    """
    Manually add or update an ingredient in the database.
    All values are per portion_g (usually 100 g).
    """

    if not name or not name.strip():
        raise ValueError("Ingredient name cannot be empty.")

    if portion_g <= 0:
        raise ValueError("Portion (g) must be greater than 0.")

    for field_name, value in {
        "energy_kj": energy_kj,
        "protein_g": protein_g,
        "carbs_g": carbs_g,
        "fat_g": fat_g,
        "fibre_g": fibre_g,
    }.items():
        if value < 0:
            raise ValueError(f"{field_name} cannot be negative.")

    insert_ingredient_information(
        name=name.strip(),
        usda_food_id=None,
        portion_g=portion_g,
        energy_kj=energy_kj,
        protein_g=protein_g,
        carbs_g=carbs_g,
        fat_g=fat_g,
        fibre_g=fibre_g,
    )
