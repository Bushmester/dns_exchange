from pymongo import MongoClient


cluster = "mongodb+srv://bushmester:Kwc3cUtCyzMfdGP@cluster0.c18sx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority&ssl=true"
db = MongoClient(cluster).dns
