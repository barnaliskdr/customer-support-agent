from pydantic import BaseModel, Field
from typing import List, Optional
from bson import ObjectId
from app.utils.objectid_util import PyObjectId

class Order(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    user_id: PyObjectId
    cart_id: PyObjectId
    status: str
    total_amount: Optional[float] = None
    delivery_address: str


model_config = {
        "json_encoders": {ObjectId: str},
        "populate_by_name": True,
        "arbitrary_types_allowed": True
    }
