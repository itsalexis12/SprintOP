from fastapi import HTTPException
from app.domain.schemas import RestaurantCreate, RestaurantUpdate
from app.repositories.restaurant_repository import RestaurantRepository


class RestaurantService:
    """Servicio encargado de la lógica de negocio y validaciones para los restaurantes."""
    def __init__(self):
        self.repository = RestaurantRepository()

    def create(self, payload: RestaurantCreate) -> dict:
        """Registra un nuevo restaurante a partir de los datos validados."""
        return self.repository.create(payload.model_dump())

    def get(self, restaurant_id: str) -> dict:
        """Obtiene un restaurante por su ID o lanza error 404 si no existe."""
        restaurant = self.repository.get(restaurant_id)
        if restaurant is None:
            raise HTTPException(status_code=404, detail="Restaurante no encontrado")
        return restaurant

    def list(
        self,
        category: str | None = None,
        city: str | None = None,
        price: int | None = None,
        order_by: str = "name",
        limit: int = 20,
        start_after: str | None = None,
    ) -> list[dict]:
        """Consulta y filtra la lista de restaurantes con soporte de ordenamiento y paginación."""
        return self.repository.list(
            category=category,
            city=city,
            price=price,
            order_by=order_by,
            limit=limit,
            start_after=start_after,
        )

    def update(self, restaurant_id: str, payload: RestaurantUpdate) -> dict:
        """Actualiza parcialmente un restaurante existente, validando que se envíen cambios."""
        data = payload.model_dump(exclude_unset=True)
        if not data:
            raise HTTPException(status_code=400, detail="No hay campos para actualizar")
        
        restaurant = self.repository.update(restaurant_id, data)
        if restaurant is None:
            raise HTTPException(status_code=404, detail="Restaurante no encontrado")
        return restaurant

    def delete(self, restaurant_id: str) -> None:
        """Elimina un restaurante por su ID o lanza error 404 si no se encuentra."""
        deleted = self.repository.delete(restaurant_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Restaurante no encontrado")