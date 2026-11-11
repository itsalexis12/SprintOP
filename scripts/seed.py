import os
from google.cloud import firestore
from google.oauth2 import service_account

PROJECT_ID = "bdfirabase-9b6c2"
CRED_PATH = "./secrets/service-account.json"

# Datos de prueba
RESTAURANTS_SEED = [
    {
        "name": "La Abuela",
        "category": "Mexicana",
        "city": "Puebla",
        "price": 2,
        "avgRating": 4.5,
        "numRatings": 20,
        "photoUrl": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5"
    },
    {
        "name": "Pizza Central",
        "category": "Pizza",
        "city": "Puebla",
        "price": 1,
        "avgRating": 4.0,
        "numRatings": 12,
        "photoUrl": "https://images.unsplash.com/photo-1513104890138-7c749659a591"
    }
]

def seed_databases():
    # 1. Crear cliente para el Emulador Local
    os.environ["FIRESTORE_EMULATOR_HOST"] = "127.0.0.1:8080"
    db_emulator = firestore.Client(project=PROJECT_ID)

    # 2. Crear cliente para la Nube (eliminando la variable del emulador)
    del os.environ["FIRESTORE_EMULATOR_HOST"]
    credentials = service_account.Credentials.from_service_account_file(CRED_PATH)
    db_cloud = firestore.Client(project=PROJECT_ID, credentials=credentials)

    print("🌱 Cargando datos en el Emulador Local y en la Nube...")

    for data in RESTAURANTS_SEED:
        # Insertar en Emulador
        ref_local = db_emulator.collection("restaurants").document()
        ref_local.set(data | {"id": ref_local.id})

        # Insertar en Nube
        ref_cloud = db_cloud.collection("restaurants").document(ref_local.id)
        ref_cloud.set(data | {"id": ref_local.id})

    print("✅ ¡Datos semilla guardados con éxito en AMBAS bases de datos!")

if __name__ == "__main__":
    seed_databases()