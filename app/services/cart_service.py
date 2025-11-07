import os
from dotenv import load_dotenv
from pymongo import MongoClient
from app.models.product_model import Product
from app.models.cart_model import Cart, CartItem
from app.services.product_service import get_product_by_id
from bson import ObjectId

# Load environment variables from the .env file
load_dotenv()

# Fetch MongoDB URL from the .env file
MONGO_URL = os.getenv("MONGO_URL")

# Create a MongoDB client
client = MongoClient(MONGO_URL)

# Access the database and collection
db = client["ecommerce_customer_agent"]         # Replace with your database name
cart_collection = db["carts"]         # Replace with your collection name


# def create_or_update_cart(user_id: str, product_id: str, quantity: int):
#     """
#     Create a cart if none exists for the user.
#     If a cart already exists, add or update the product in the cart.
#     """
#     # ✅ Check if cart exists for the user
#     existing_cart = cart_collection.find_one({"user_id": ObjectId(user_id)})

#     # ✅ Fetch product info
#     product_data = get_product_by_id(product_id)
#     if not product_data:
#         raise ValueError(f"Product with id {product_id} not found")

#     # Build CartItem
#     cart_item = CartItem(product=Product(**product_data), quantity=quantity)

#     # ✅ If no existing cart, create new
#     if not existing_cart:
#         new_cart = Cart(
#             user_id=ObjectId(user_id),
#             items=[cart_item],
#             total_price=cart_item.product.price * quantity
#         )
#         result = cart_collection.insert_one(new_cart.dict(by_alias=True))
#         new_cart.id = result.inserted_id
#         return new_cart

#     # ✅ If cart exists, check if product already in cart
#     for item in existing_cart["items"]:
#         if item["product"]["_id"] == ObjectId(product_id):
#             item["quantity"] += quantity
#             break
#     else:
#         # Product not in cart, add it
#         existing_cart["items"].append(cart_item.dict(by_alias=True))

#     # ✅ Recalculate total price
#     total_price = 0.0
#     for item in existing_cart["items"]:
#         total_price += item["product"]["price"] * item["quantity"]

#     existing_cart["total_price"] = total_price

#     # ✅ Update cart in DB
#     cart_collection.update_one(
#         {"_id": existing_cart["_id"]},
#         {"$set": {"items": existing_cart["items"], "total_price": total_price}}
#     )

#     return Cart(**existing_cart)


def create_or_update_cart(user_id: str, product_id: str, quantity: int):
    """
    Create a cart if none exists for the user.
    If a cart already exists, add or update the product in the cart.
    """

    # ✅ Check if cart exists for the user
    existing_cart = cart_collection.find_one({"user_id": ObjectId(user_id)})

    # ✅ Fetch product info
    product_data = get_product_by_id(product_id)
    if not product_data:
        raise ValueError(f"Product with id {product_id} not found")

    # ✅ Safely handle both dict and Product model cases
    product = product_data if isinstance(product_data, Product) else Product(**product_data)

    # ✅ Create cart item
    cart_item = CartItem(product=product, quantity=quantity)

    # ✅ If no existing cart, create a new one
    if not existing_cart:
        new_cart = Cart(
            user_id=ObjectId(user_id),
            items=[cart_item],
            total_price=cart_item.product.price * quantity
        )
        result = cart_collection.insert_one(new_cart.dict(by_alias=True))
        new_cart.id = result.inserted_id
        return new_cart

    # ✅ If cart exists, check if product already in cart
    for item in existing_cart["items"]:
        if str(item["product"]["_id"]) == str(product_id):
            item["quantity"] += quantity
            break
    else:
        # Product not in cart → add it
        existing_cart["items"].append(cart_item.dict(by_alias=True))

    # ✅ Recalculate total price
    total_price = sum(
        item["product"]["price"] * item["quantity"]
        for item in existing_cart["items"]
    )
    existing_cart["total_price"] = total_price

    # ✅ Update in DB
    cart_collection.update_one(
        {"_id": existing_cart["_id"]},
        {"$set": {"items": existing_cart["items"], "total_price": total_price}}
    )

    # ✅ Return updated cart as a Pydantic model
    return Cart(**existing_cart)




def remove_from_cart(user_id: str, product_id: str, quantity: int):
    """
    Remove or decrement a product from the user's cart.
    - If quantity > 0: decreases the product quantity.
    - If quantity <= 0 or resulting quantity <= 0: removes the product from cart.
    - If the cart becomes empty, it deletes the cart document.
    """

    # ✅ Fetch the user's existing cart
    existing_cart = cart_collection.find_one({"user_id": ObjectId(user_id)})
    if not existing_cart:
        raise ValueError("Cart not found for this user.")

    # ✅ Find the product inside the cart
    product_found = False
    for item in existing_cart["items"]:
        if str(item["product"]["_id"]) == str(product_id):
            product_found = True
            item["quantity"] -= quantity
            # If the item’s quantity drops to zero or below, remove it
            if item["quantity"] <= 0:
                existing_cart["items"].remove(item)
            break

    if not product_found:
        raise ValueError(f"Product with id {product_id} not found in cart.")

    # ✅ If cart is now empty, delete the whole document
    if not existing_cart["items"]:
        cart_collection.delete_one({"_id": existing_cart["_id"]})
        return {"message": "Cart is now empty and has been deleted."}

    # ✅ Recalculate total price
    total_price = sum(
        item["product"]["price"] * item["quantity"]
        for item in existing_cart["items"]
    )
    existing_cart["total_price"] = total_price

    # ✅ Update the cart in MongoDB
    cart_collection.update_one(
        {"_id": existing_cart["_id"]},
        {"$set": {"items": existing_cart["items"], "total_price": total_price}}
    )

    # ✅ Return updated cart as Pydantic model
    return Cart(**existing_cart)


def fetch_cart_details(user_id: str):
    print("Fetching cart details for user_id:", user_id)

    """
    Fetch the cart details for a given user.
    - Returns the user's current cart as a Pydantic model.
    - If no cart exists, returns a friendly message.
    """

    # ✅ Find the cart document for the user
    existing_cart = cart_collection.find_one({"user_id": ObjectId(user_id)})

    if not existing_cart:
        return {"message": "No active cart found for this user."}

    # ✅ Convert MongoDB document to Cart Pydantic model
    return Cart(**existing_cart)
