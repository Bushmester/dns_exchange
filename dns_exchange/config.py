import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

HOST = '0.0.0.0'
PORT = 8106
MONGO_DB_LINK = os.getenv('MONGO_DB_LINK')
WORDS_LINK = os.getenv('WORDS_LINK')
