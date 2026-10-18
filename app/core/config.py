from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "FriendlyEats FastAPI"
    ENVIRONMENT: str = "local"
    FIREBASE_PROJECT_ID: str
    FIREBASE_CREDENTIALS_PATH: str | None = None
    FIRESTORE_EMULATOR_HOST: str | None = None

    class Config:
        env_file = ".env"

settings = Settings()