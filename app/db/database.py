from pymongo import mongo_client, ASCENDING
from pymongo.errors import PyMongoError

from app.core.config import settings

client = mongo_client.MongoClient(settings.MONGODB_URI)
print('🚀 Connected to MongoDB...')

db = client[settings.MONGO_INITDB_DATABASE]
User = db.users
User.create_index([("email", ASCENDING)], unique=True)


def init_database() -> None:
    try:
        conn = client.server_info()
        print(f'Connected to MongoDB {conn.get("version")}')
    except PyMongoError as e:
        print(f"Unable to connect to the MongoDB server: {e}")
