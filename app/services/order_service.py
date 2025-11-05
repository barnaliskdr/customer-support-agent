import os
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient
from bson import ObjectId
from fastapi import HTTPException

from app.models.order_model import Order

# Load env and DB
load_dotenv()
MONGO_URL = os.getenv("MONGO_URL")
client = MongoClient(MONGO_URL)
db = client["ecommerce_customer_agent"]
carts_collection = db["carts"]
orders_collection = db["orders"]

def place_order(user_id: str, cart_id: str, delivery_address: str, delete_cart: bool = True) -> Order:
    """
    Create an Order from a user's cart.
    - Validates cart existence and ownership.
    - Reads total from cart (falls back to computing it).
    - Inserts order into orders collection.
    - Optionally deletes the cart after placing the order.
    Returns: Order Pydantic model.
    Raises HTTPException on errors.
    """
    try:
        uid = ObjectId(user_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid user_id")

    try:
        cid = ObjectId(cart_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid cart_id")

    cart_doc = carts_collection.find_one({"_id": cid})
    if not cart_doc:
        raise HTTPException(status_code=404, detail="Cart not found")

    # Ensure cart belongs to user
    cart_user = cart_doc.get("user_id")
    if cart_user is None or str(cart_user) != str(uid):
        raise HTTPException(status_code=403, detail="Cart does not belong to user")

    items = cart_doc.get("items", [])
    if not items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    # Determine total_amount (prefer stored total_price)
    total_amount = cart_doc.get("total_price")
    if total_amount is None:
        # compute if not present
        try:
            total_amount = sum(
                float(item["product"]["price"]) * int(item.get("quantity", 0))
                for item in items
            )
        except Exception:
            raise HTTPException(status_code=500, detail="Failed to compute cart total")

    order_doc = {
        "user_id": uid,
        "cart_id": cid,
        "status": "placed",
        "total_amount": float(total_amount),
        "delivery_address": delivery_address,
        "created_at": datetime.utcnow()
    }

    res = orders_collection.insert_one(order_doc)
    order_doc["_id"] = res.inserted_id

    if delete_cart:
        carts_collection.delete_one({"_id": cid})

    # return Pydantic model (uses model_validate for pydantic v2)
    return Order.model_validate(order_doc)

def get_order_by_id(order_id: str) -> Order:
    try:
        oid = ObjectId(order_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid order_id")

    order_doc = orders_collection.find_one({"_id": oid})
    if not order_doc:
        raise HTTPException(status_code=404, detail="Order not found")

    return Order.model_validate(order_doc)