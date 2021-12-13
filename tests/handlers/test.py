import pymongo
from pymongo import MongoClient

import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context


cluster = MongoClient("mongodb+srv://eale:novode25@eale.rgtbh.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["dns"]
collection = db["users"]

post = {"id": 0}

collection.insert_one(post)
