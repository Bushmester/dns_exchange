from pymongo import MongoClient


cluster = "mongodb+srv://username:password@cluster0.c18sx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority&ssl=true"
db = MongoClient(cluster).dns
