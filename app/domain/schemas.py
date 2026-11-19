from pydantic import BaseModel, Field
class RestaurantBase(BaseModel):
    """Esquema base con los atributos principales y validaciones de un restaurante."""
    name: str = Field(min_length=1, max_length=100)
    category: str = Field(min_length=1, max_length=50)
    city: str = Field(min_length=1, max_length=50)
    price: int = Field(ge=1, le=3)
    photoUrl: str | None = None
class RestaurantCreate(RestaurantBase):
    """Esquema utilizado para validar los datos al registrar un nuevo restaurante."""
    pass
class RestaurantUpdate(BaseModel):
    """Esquema con campos opcionales para actualizar parcialmente un restaurante."""
    name: str | None = Field(default=None, min_length=1, max_length=100)
    category: str | None = Field(default=None, min_length=1, max_length=50)
    city: str | None = Field(default=None, min_length=1, max_length=50)
    price: int | None = Field(default=None, ge=1, le=3)
    photoUrl: str | None = None
class RestaurantResponse(RestaurantBase):
    """Esquema de respuesta que incluye el ID y las métricas de calificación."""
    id: str
    avgRating: float = 0
    numRatings: int = 0