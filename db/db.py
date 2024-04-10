import os
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")


class DataBase:
    client: AsyncIOMotorClient = None


db = DataBase()


def get_database():
    return db.client["pipe"]


def get_collection(collection: str):
    database = get_database()
    return database.get_collection(collection)


async def connect_to_mongo():
    db.client = AsyncIOMotorClient(MONGO_URL)  # Adjust the connection string as needed


async def close_mongo_connection():
    db.client.close()


def create_start_app_handler(app: FastAPI) -> callable:
    async def start_app() -> None:
        await connect_to_mongo()
    return start_app


def create_stop_app_handler(app: FastAPI) -> callable:
    async def stop_app() -> None:
        await close_mongo_connection()
    return stop_app
