from pymongo import MongoClient
from app.config import settings

# Config database
client = MongoClient(settings.DATABSE_URL)
db = client.urls
collection = db.urls
