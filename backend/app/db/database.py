from pymongo import MongoClient
from app.config import settings

# Config database
client = MongoClient(settings.DATABSE_URL)

db = client.links
link_collection = db.urls
user_collection = db.user
