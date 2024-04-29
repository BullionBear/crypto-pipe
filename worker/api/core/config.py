from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    worker_name: str = os.getenv("WORKER_NAME", "worker")
    database_url: str = os.getenv("MONGO_URL", "mongodb://localhost:27017")

