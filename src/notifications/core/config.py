from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
import os
from pathlib import Path

#variables globales de configuración

class Settings(BaseSettings):

    #EMAIL_ENABLED: bool = True
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )

    MONGO_CONNECTION_STRING: str = os.getenv("MONGO_CONNECTION_STRING", "mongodb://localhost:27017")
    MONGO_DATABASE_NAME: str = os.getenv("MONGO_DATABASE_NAME", "notifications_db")

    SENDGRID_API_KEY: str = os.getenv("SENDGRID_API_KEY")
    SENDGRID_FROM_EMAIL: str = os.getenv("SENDGRID_FROM_EMAIL")
    SENDGRID_LOCAL_MODE: bool = True #os.getenv("SENDGRID_LOCAL_MODE", "false").lower() == "true"
    
    LOG_LEVEL: str = "DEBUG"
    LOG_FILE: str = "log.txt"
    LOG_BACKUP_COUNT: int = 7


settings = Settings()