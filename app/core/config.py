from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Configuración global de la aplicación cargada desde variables de entorno."""
    APP_NAME: str = "FriendlyEats FastAPI"
    ENVIRONMENT: str = "local"
    FIREBASE_PROJECT_ID: str
    FIREBASE_CREDENTIALS_PATH: str | None = None
    FIRESTORE_EMULATOR_HOST: str | None = None

    class Config:
        """Indica el archivo local desde donde se leen las variables de entorno."""
        env_file = ".env"
# Instancia global de configuración disponible para toda la aplicación
settings = Settings()