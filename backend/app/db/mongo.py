from pymongo import MongoClient

client = MongoClient("mongodb://mongo:27017")

db = client["ims_db"]
signals_collection = db["signals"]
