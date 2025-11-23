from pydantic_settings import BaseSettings, SettingsConfigDict

#variables globales de configuración

class Settings(BaseSettings):
    
    # Default settings
    MONGO_CONNECTION_STRING: str = "mongodb://localhost:27017"
    MONGO_DATABASE_NAME: str = "notifications_db"
    
    LOG_LEVEL: str = "DEBUG"
    LOG_FILE: str = "log.txt"
    LOG_BACKUP_COUNT: int = 7
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )

settings = Settings()
