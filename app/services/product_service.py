import os
from dotenv import load_dotenv
from pymongo import MongoClient
from app.models.product_model import Product

# Load environment variables from the .env file
load_dotenv()

# Fetch MongoDB URL from the .env file
MONGO_URL = os.getenv("MONGO_URL")

# Create a MongoDB client
client = MongoClient(MONGO_URL)

# Access the database and collection
db = client["ecommerce_customer_agent"]         # Replace with your database name
collection = db["products"]         # Replace with your collection name


def get_all_products():
    """
    Fetch all products from MongoDB.
    Each product is converted from BSON to a Python dict, 
    and the '_id' field is converted to a string for JSON serialization.
    """
    try:
        # Fetch all product documents
        products_cursor = collection.find()

        # Convert cursor to list of dictionaries
        products = []
        for product in products_cursor:
            product["_id"] = str(product["_id"])  # Convert ObjectId to string
            products.append(product)
        return products

    except Exception as e:
        print("Error fetching products:", e)
        return []

# def get_product_by_id(product_id: int):
#     # Example logic (in a real app, query DB here)
#     product = {"id": product_id, "name": f"Product {product_id}", "price": 5000 + product_id * 100}
#     return product


# def get_product_by_name(product_name: str):
#     # Example logic (in a real app, query DB here)
#     product = {"id": 1, "name": product_name, "price": 6000}
#     return product


def get_product_by_name(prod_name: str) -> list:
    """
    Fetch products from MongoDB by exact or partial name match (case-sensitive).
    Returns a list of Product objects that match or are similar to the given name.
    """
    try:
        # Case-sensitive regex match (no "$options": "i")
        query = {"name": {"$regex": prod_name}}

        products_cursor = collection.find(query)
        print("products_cursor", products_cursor)
        products = [Product(**prod) for prod in products_cursor]

        if not products:
            print(f"No products found matching '{prod_name}'.")
        return products

    except Exception as e:
        print("Error while fetching products:", e)
        return []
