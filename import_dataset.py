import pandas as pd
from pymongo import MongoClient
from config import Config

client = MongoClient(Config.MONGO_URI)
db = client.stroke_db
collection = db.patients

df = pd.read_csv("healthcare-dataset-stroke-data.csv")
collection.insert_many(df.to_dict("records"))

print("Dataset imported successfully")
