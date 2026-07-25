import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Banking Customer Segmentation Agent"
    DATASET_PATH: str = os.path.join(os.path.dirname(__file__), "..", "data_store", "customer_banking_data.csv")
    DB_PATH: str = "sqlite_state.db"
    GROQ_API_KEY: str   
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()