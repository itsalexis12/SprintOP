from google.cloud.firestore_v1.base_query import FieldFilter
from app.core.firebase import db


class RestaurantRepository:
    """Repositorio encargado de realizar las operaciones CRUD en la colección de restaurantes de Firestore."""

    def __init__(self):
        self.collection = db.collection("restaurants")

    def create(self, data: dict) -> dict:
        """Crea un nuevo documento de restaurante con ID autogenerado y métricas inicializadas."""
        # Genera una referencia vacía para obtener un ID automático antes de guardar
        ref = self.collection.document()
        data["id"] = ref.id
        data["avgRating"] = 0
        data["numRatings"] = 0
        ref.set(data)
        return data

    def get(self, restaurant_id: str) -> dict | None:
        """Busca y devuelve un restaurante por su ID, o None si no existe."""
        doc = self.collection.document(restaurant_id).get()
        if not doc.exists:
            return None
        return doc.to_dict() | {"id": doc.id}

    def list(
        self,
        category: str | None = None,
        city: str | None = None,
        price: int | None = None,
        order_by: str = "name",
        limit: int = 20,
        start_after: str | None = None,
    ) -> list[dict]:
        """Consulta restaurantes aplicando filtros opcionales, ordenamiento y paginación por cursor."""
        query = self.collection

        if category:
            query = query.where(filter=FieldFilter("category", "==", category))
        if city:
            query = query.where(filter=FieldFilter("city", "==", city))
        if price:
            query = query.where(filter=FieldFilter("price", "==", price))

        query = query.order_by(order_by).limit(limit)

        if start_after:
            last_doc = self.collection.document(start_after).get()
            if last_doc.exists:
                query = query.start_after(last_doc)

        return [doc.to_dict() | {"id": doc.id} for doc in query.stream()]

    def update(self, restaurant_id: str, data: dict) -> dict | None:
        """Actualiza los campos indicados de un restaurante existente y devuelve el registro actualizado."""
        ref = self.collection.document(restaurant_id)
        doc = ref.get()
        if not doc.exists:
            return None
        ref.update(data)
        return self.get(restaurant_id)

    def delete(self, restaurant_id: str) -> bool:
        """Elimina un restaurante por su ID y devuelve True si existía."""
        ref = self.collection.document(restaurant_id)
        doc = ref.get()
        if not doc.exists:
            return False
        ref.delete()
        return True