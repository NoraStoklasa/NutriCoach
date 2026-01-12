import requests
from config import USDA_API_KEY, USDA_SEARCH_URL
from database import create_table


def search_ingredient(ingredient_name):
    """Search for an ingredient in the USDA database and return the first matching food item"""

    # params sent to the API
    params = {
        "query": ingredient_name,
        "api_key": USDA_API_KEY,
        "pageSize": 1,  # number of results
        "dataType": ["Foundation", "SR Legacy"],
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
    """Extract relevant nutrients from food data (searched food item) returned by USDA API"""

    # Nutrient map of IDs to database columns
    nutrient_map = {
        1062: "energy_kj",  # Energy, kJ
        1003: "protein_g",  # Protein
        1005: "carbs_g",  # Carbohydrate, by difference
        1004: "fat_g",  # Total lipid (fat)
        1079: "fibre_g",  # Fiber, total dietary
    }

    nutrients = {}

    # Extract the nutrients from the food data list
    for nutrient in food_data.get(
        "foodNutrients", []
    ):  # foodNutrients is a list of dicts of nutrients for the ingredient, else return empty list to prevent errors
        nutrient_id = nutrient.get("nutrientId")
        if nutrient_id in nutrient_map:
            nutrients[nutrient_map[nutrient_id]] = nutrient.get(
                "value"
            )  # getting the id's value=column name and the value for the key

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
