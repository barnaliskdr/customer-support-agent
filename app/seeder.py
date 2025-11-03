# import json
# from pymongo import MongoClient
# from dotenv import load_dotenv
# import os

# # Load MongoDB URL
# load_dotenv()
# MONGO_URL = os.getenv("MONGO_URL")

# client = MongoClient(MONGO_URL)
# print("Connected to MongoDB",MONGO_URL)
# db = client["ecommerce_customer_agent"]       # your DB name
# collection = db["products"]       # your collection name

# # Read data from JSON file
# with open("products.json", "r") as f:
#     products = json.load(f)

# # Insert into MongoDB
# result = collection.insert_many(products)
# print(f"{len(result.inserted_ids)} products inserted successfully!")

import json
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load MongoDB URL
load_dotenv()
MONGO_URL = os.getenv("MONGO_URL")

print(f"Connected to MongoDB {MONGO_URL}")

client = MongoClient(MONGO_URL)
db = client["ecommerce_customer_agent"]
collection = db["products"]

# ✅ Use full path
json_path = r"D:\Customer_Support_Agent\app\products.json"

with open(json_path, "r") as f:
    products = json.load(f)

result = collection.insert_many(products)
print(f"{len(result.inserted_ids)} products inserted successfully!")




# Command to run the seeder file  
#  python "D:\Customer_Support_Agent\app\seeder.py"