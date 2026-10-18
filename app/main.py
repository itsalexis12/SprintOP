from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.v1.restaurants import router as restaurants_router
from app.services.restaurant_service import RestaurantService

app = FastAPI(title="FriendlyEats FastAPI")

# Endpoints de la API JSON
app.include_router(restaurants_router, prefix="/api/v1")

# Archivos estáticos y plantillas Jinja2
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="app/templates")
service = RestaurantService()


@app.get("/health")
async def health():
    return {"status": "ok"}


# 1. LISTADO PRINCIPAL
@app.get("/")
async def home(
    request: Request,
    city: str | None = None,
    category: str | None = None,
    price: int | None = None,
):
    restaurants = service.list(city=city, category=category, price=price)
    return templates.TemplateResponse(
        request=request,
        name="restaurants.html",
        context={"restaurants": restaurants},
    )


# 2. FORMULARIO NUEVO (DEBE IR ANTES DE /{restaurant_id})
@app.get("/restaurants/new")
async def new_restaurant_form(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="restaurant_form.html",
        context={"restaurant": None},
    )


# 3. VER DETALLE DE RESTAURANTE
@app.get("/restaurants/{restaurant_id}")
async def restaurant_detail(request: Request, restaurant_id: str):
    try:
        restaurant = service.get(restaurant_id)
        return templates.TemplateResponse(
            request=request,
            name="restaurant_detail.html",
            context={"restaurant": restaurant},
        )
    except HTTPException:
        raise HTTPException(status_code=404, detail="Restaurante no encontrado")


# 4. FORMULARIO EDITAR
@app.get("/restaurants/{restaurant_id}/edit")
async def edit_restaurant_form(request: Request, restaurant_id: str):
    try:
        restaurant = service.get(restaurant_id)
        return templates.TemplateResponse(
            request=request,
            name="restaurant_form.html",
            context={"restaurant": restaurant},
        )
    except HTTPException:
        raise HTTPException(status_code=404, detail="Restaurante no encontrado")