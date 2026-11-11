import os
from google.cloud import firestore
from google.oauth2 import service_account
from dotenv import load_dotenv

load_dotenv()

cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH")
project_id = os.getenv("FIREBASE_PROJECT_ID")
emulator_host = os.getenv("FIRESTORE_EMULATOR_HOST")

if emulator_host:
    # 1. MODO LOCAL: Asegura la variable en el entorno global para el SDK
    os.environ["FIRESTORE_EMULATOR_HOST"] = emulator_host
    db = firestore.Client(project=project_id)
elif cred_path and os.path.exists(cred_path):
    # 2. MODO NUBE: Carga explícitamente las credenciales de la llave JSON
    credentials = service_account.Credentials.from_service_account_file(cred_path)
    db = firestore.Client(project=project_id, credentials=credentials)
else:
    raise RuntimeError(
        "Error de conexión: Revisa tu .env. Debes tener FIRESTORE_EMULATOR_HOST activo "
        "o la llave 'service-account.json' existente en la ruta especificada."
    )