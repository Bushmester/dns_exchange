from pymongo import MongoClient
from redis import Redis
from dns_exchange.config import MONGO_DB_LINK


# MongoDB init
cluster = MONGO_DB_LINK
client = MongoClient(cluster)
db = client.dns

# Redis init
redis_db = Redis()
