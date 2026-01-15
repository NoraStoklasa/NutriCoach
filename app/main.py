from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.routes.ingredients import router as ingredients_router
from app.routes.recipes import router as recipes_router


app = FastAPI(title="NutriCoach")

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
def home():
    return {"status": "NutriCoach API is running"}


# Registering routers
app.include_router(ingredients_router)
app.include_router(recipes_router)
