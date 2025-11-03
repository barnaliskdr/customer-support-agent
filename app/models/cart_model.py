# app/models/cart_model.py
from pydantic import BaseModel, Field
from typing import List, Optional
from utils.objectid_util import PyObjectId
from models.product_model import Product  # relative import if models in same folder

class CartItem(BaseModel):
    product: Product
    quantity: int

class Cart(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId
    items: List[CartItem] = []
    total_price: Optional[float] = 0.0

class Config:
    allow_population_by_field_name = True
    json_encoders = {PyObjectId: str}