from fastapi import APIRouter, FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
import sqlite3

from ingredients.manual_ingredient import add_ingredient_manually

from config import DB_PATH

router = APIRouter(prefix="/ingredients")
templates = Jinja2Templates(directory="app/templates")


# Route to list all ingredients from the database
@router.get("")
def list_ingredients(request: Request):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM ingredients ORDER by name")
        ingredients = [row[0] for row in cursor.fetchall()]
    return templates.TemplateResponse(
        "ingredients_list.html", {"request": request, "ingredients": ingredients}
    )


# Route to show the form for adding a new ingredient
@router.get("/new")
def new_ingredient_form(request: Request):
    return templates.TemplateResponse("ingredient_form.html", {"request": request})


# Route to handle the submission of a new ingredient
@router.post("/new")
def create_ingredient(
    name: str = Form(...),
    portion_g: float = Form(...),
    energy_kj: float = Form(...),
    protein_g: float = Form(...),
    carbs_g: float = Form(...),
    fat_g: float = Form(...),
    fibre_g: float = Form(...),
):
    add_ingredient_manually(
        name=name,
        portion_g=portion_g,
        energy_kj=energy_kj,
        protein_g=protein_g,
        carbs_g=carbs_g,
        fat_g=fat_g,
        fibre_g=fibre_g,
    )

    return RedirectResponse(
        url="/ingredients",
        status_code=303,
    )
