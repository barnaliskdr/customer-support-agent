import os
from dotenv import load_dotenv
from pymongo import MongoClient
from bson import ObjectId
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


def get_product_by_category(prod_category: str) -> list:
    """
    Fetch products from MongoDB by exact or partial name match (case-sensitive).
    Returns a list of Product objects that match or are similar to the given name.
    """
    try:
        query = {"category": {"$regex": f"^{prod_category}$", "$options": "i"}}

        # ^ and $ make it match the entire string, just like $eq.

        # $options: "i" makes it case-insensitive.

        # "fashion", "Fashion", "FASHION" → all match.

        products_cursor = collection.find(query)
        print("products_cursor", products_cursor)
        products = [Product(**prod) for prod in products_cursor]

        if not products:
            print(f"No products found matching '{prod_category}'.")
        return products

    except Exception as e:
        print("Error while fetching products:", e)
        return []


def get_product_by_id(product_id: str) -> dict:
    """
    Fetch a single product by its ObjectId.
    Returns the product as a dictionary or None if not found.
    """
    try:
        if not ObjectId.is_valid(product_id):
            raise ValueError(f"Invalid ObjectId: {product_id}")

        product = collection.find_one({"_id": ObjectId(product_id)})

        if product:
            product["_id"] = str(product["_id"])  # Convert ObjectId for JSON
            return product
        else:
            print(f"No product found with id '{product_id}'.")
            return None
    except Exception as e:
        print("Error while fetching product by ID:", e)
        return None