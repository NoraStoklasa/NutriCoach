import os
from dotenv import load_dotenv

load_dotenv()

USDA_SEARCH_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"
DB_PATH = "ingredients.db"

USDA_API_KEY = os.getenv("USDA_API_KEY")
