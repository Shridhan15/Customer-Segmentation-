import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Banking Customer Segmentation Agent"
    DATASET_PATH: str = os.path.join("data_store", "customers.csv")
    DB_PATH: str = "sqlite_state.db"
    GROQ_API_KEY: str   
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()