from bson import ObjectId
from typing import Optional, Union
from pydantic import BaseModel, Field
from app.utils.objectid_util import PyObjectId

@classmethod
def create_from_cart(cls,
                         user_id: Union[str, PyObjectId],
                         cart_id: Union[str, PyObjectId],
                         db,
                         status: str = "pending",
                         delivery_address: str = "") -> "Order":
        """
        Build an Order instance using cart details fetched from the DB.
        - db is expected to be a PyMongo database/client with a `carts` collection.
        - cart_id and user_id may be either str or PyObjectId.
        """
        uid = ObjectId(user_id) if isinstance(user_id, str) else user_id
        cid = ObjectId(cart_id) if isinstance(cart_id, str) else cart_id

        cart_doc = db.carts.find_one({"_id": cid})
        if not cart_doc:
            raise ValueError("Cart not found for cart_id")

        total = cart_doc.get("total_price", 0.0)

        return cls(
            user_id=uid,
            cart_id=cid,
            status=status,
            total_amount=total,
            delivery_address=delivery_address
        )