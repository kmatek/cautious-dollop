from pymongo import MongoClient
from ..settings import DATABSE_URL

# Config database
client = MongoClient(DATABSE_URL)
db = client.urls
collection = db.urls
