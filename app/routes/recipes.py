from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import sqlite3

from recipes.recipe_database import create_recipe, load_recipe, add_recipe_ingredient
from ingredients.database import get_all_ingredient_names
from logic.recalculate_nutrients import recalculate_nutrients


from config import RECIPE_DB_PATH

router = APIRouter(prefix="/recipes")
templates = Jinja2Templates(directory="app/templates")


# Route to list all recipes from the database
@router.get("")
def list_recipes(request: Request):
    with sqlite3.connect(RECIPE_DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT id, name, category
            FROM recipes
            ORDER BY category, name
        """
        )
        recipes = cur.fetchall()

    return templates.TemplateResponse(
        "recipes_list.html",
        {
            "request": request,
            "recipes": recipes,
        },
    )


# Route to show the form for adding a new recipe
@router.get("/new")
def new_recipe_form(request: Request):
    return templates.TemplateResponse(
        "recipe_form.html",
        {"request": request},
    )


# Route to handle the submission of a new recipe
@router.post("/new")
def create_recipe_post(
    name: str = Form(...),
    category: str = Form(...),
    instructions: str = Form(...),
    image_path: str = Form(""),
):
    create_recipe(
        name=name,
        category=category,
        instructions=instructions,
        image_path=image_path,
    )

    return RedirectResponse(
        url="/recipes",
        status_code=303,
    )


# Route to show the details of a specific recipe
@router.get("/{recipe_id}")
def recipe_detail(request: Request, recipe_id: int):
    recipe = load_recipe(recipe_id)
    ingredients = get_all_ingredient_names()

    nutrients = recalculate_nutrients(recipe)

    return templates.TemplateResponse(
        "recipe_detail.html",
        {
            "request": request,
            "recipe": recipe,
            "ingredients": ingredients,
            "nutrients": nutrients,
        },
    )


# Route to handle adding an ingredient to a specific recipe
@router.post("/{recipe_id}")
def add_ingredient_to_recipe(
    recipe_id: int,
    ingredient_name: str = Form(...),
    portion_g: float = Form(...),
):
    add_recipe_ingredient(
        recipe_id=recipe_id,
        ingredient_name=ingredient_name,
        portion_g=portion_g,
    )

    return RedirectResponse(
        url=f"/recipes/{recipe_id}",
        status_code=303,
    )
