from database.connect import Settings, conn_mongo

# Settings 클래스를 인스턴스화 해서 .env 값을 가져온다.
settings = Settings()

# SQLAlchemy를 사용하는 경우
MONGODB_URL = f"mongodb://{settings.DB_USER}:{settings.DB_PWD}@{settings.MONGODB_HOST}:{27017}/?authSource={settings.DB_USER}"

mongo_conn = conn_mongo(MONGODB_URL)
