from pymongo import MongoClient
from ..config import settings

# Config database
client = MongoClient(settings.DATABSE_URL)
db = client.urls
collection = db.urls
