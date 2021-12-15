import logging
import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# Server config
HOST = '0.0.0.0'
PORT = 8121
LOGGING_LEVEL = logging.DEBUG

# App config
COMMISSION = 0.001

# environment variables
MONGO_DB_LINK = os.getenv('MONGO_DB_LINK')
WORDS_LINK = os.getenv('WORDS_LINK')
