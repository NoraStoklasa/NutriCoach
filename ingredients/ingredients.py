"""Functions to interact with the USDA FoodData Central API to search for ingredients and extract nutrient information"""

import requests
from config import USDA_API_KEY, USDA_SEARCH_URL


def search_ingredient(ingredient_name):
    """Search for an ingredient in the USDA database and return the first matching food item"""

    # params sent to the API
    params = {
        "query": ingredient_name,
        "api_key": USDA_API_KEY,
        "pageSize": 1,  # number of results
        "dataType": ["Foundation", "SR Legacy", "Branded"],  # types of data to include
    }

    # send request
    response = requests.get(USDA_SEARCH_URL, params=params)

    response.raise_for_status()  # error protection

    # converts raw text to foods list
    foods = response.json().get("foods", [])
    if not foods:
        return None

    return foods[0]  # return the first food item


def extract_nutrients(food_data):
    """
    Decide how to extract nutrients based on USDA data type
    """
    data_type = food_data.get("dataType")

    if data_type in ("Foundation", "SR Legacy"):
        return extract_nutrients_foundation(food_data)

    if data_type == "Branded":
        return extract_nutrients_branded(food_data)

    return {}


def _ensure_energy_kj(nutrients):
    if nutrients.get("energy_kj") is None:
        protein_g = nutrients.get("protein_g") or 0
        carbs_g = nutrients.get("carbs_g") or 0
        fat_g = nutrients.get("fat_g") or 0
        fibre_g = nutrients.get("fibre_g") or 0
        nutrients["energy_kj"] = (
            protein_g * 17 + carbs_g * 17 + fat_g * 37 + fibre_g * 8
        )


def extract_nutrients_foundation(food_data):
    """Extract nutrients from Foundation or SR Legacy foods"""

    nutrient_map = {
        1062: "energy_kj",  # Energy (kJ)
        1008: "energy_kcal",  # Energy (kcal) - need to convert
        1003: "protein_g",  # Protein
        1005: "carbs_g",  # Carbohydrate
        1004: "fat_g",  # Fat
        1079: "fibre_g",  # Fibre
    }

    nutrients = {
        "energy_kj": None,
        "protein_g": None,
        "carbs_g": None,
        "fat_g": None,
        "fibre_g": None,
    }

    for nutrient in food_data.get("foodNutrients", []):
        nutrient_id = nutrient.get("nutrientId")
        value = nutrient.get("value")
        if nutrient_id in nutrient_map:
            if nutrient_id == 1008:  # Convert kcal to kJ
                nutrients["energy_kj"] = value * 4.184 if value is not None else None
            elif nutrient_id == 1062:
                nutrients["energy_kj"] = value
            else:
                nutrients[nutrient_map[nutrient_id]] = value

    _ensure_energy_kj(nutrients)
    return nutrients


def extract_nutrients_branded(food_data):
    """Extract nutrients from Branded foods"""

    nutrients = {
        "energy_kj": None,
        "protein_g": None,
        "carbs_g": None,
        "fat_g": None,
        "fibre_g": None,
    }

    starch = None
    sugars = None

    for nutrient in food_data.get("foodNutrients", []):
        nutrient_id = nutrient.get("nutrientId")
        value = nutrient.get("value")

        if nutrient_id == 1062:  # Energy (kJ)
            nutrients["energy_kj"] = value
        elif nutrient_id == 1008:  # Energy (kcal) - convert to kJ
            nutrients["energy_kj"] = value * 4.184 if value is not None else None
        elif nutrient_id == 1003:  # Protein
            nutrients["protein_g"] = value
        elif nutrient_id == 1004:  # Fat
            nutrients["fat_g"] = value
        elif nutrient_id == 1005:  # Carbohydrate
            nutrients["carbs_g"] = value
        elif nutrient_id == 1079:  # Fibre
            nutrients["fibre_g"] = value
        elif nutrient_id == 1009:  # Starch
            starch = value
        elif nutrient_id == 2000:  # Total sugars
            sugars = value

    # Build carbs, fibre and energy_kj if missing
    if nutrients.get("carbs_g") is None:
        nutrients["carbs_g"] = (starch or 0) + (sugars or 0)
    if nutrients.get("fibre_g") is None:
        nutrients["fibre_g"] = 0.0
    _ensure_energy_kj(nutrients)

    return nutrients


def extract_portion(food_data):
    """Extract portion size in grams from food measures"""

    measures = food_data.get("foodMeasures", [])
    if measures:
        # Get the first measure which is typically the serving size
        first_measure = measures[0]
        # Return gram weight if available
        gram_weight = first_measure.get("gramWeight")
        if gram_weight:
            return gram_weight

    # Default to 100g if no measure found
    return 100.0


def extract_usda_food_id(food_data):
    """Extract USDA FoodData Central ID from food data."""
    return food_data.get("fdcId")
