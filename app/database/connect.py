from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient
from pydantic_settings import BaseSettings


# Setting config load
class Settings(BaseSettings):
    SERVER_SECRET_KEY: Optional[str] = None
    DB_USER: Optional[str] = None
    DB_PWD: Optional[str] = None
    MONGODB_HOST: Optional[str] = None

    class Config:
        env_file = ".env"


def conn_mongo(engine_url) -> AsyncIOMotorClient:
    print("MongoDB 연결 되었습니다.")
    return AsyncIOMotorClient(engine_url)
