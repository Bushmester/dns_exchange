import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

HOST = '0.0.0.0'
PORT = 8090
MONGO_DB_LINK = os.getenv('MONGO_DB_LINK')
