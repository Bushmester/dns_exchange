from pymongo import MongoClient

from dns_exchange.config import MONGO_DB_LINK

cluster = MONGO_DB_LINK
db = MongoClient(cluster).dns
