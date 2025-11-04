from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services import cart_service

router = APIRouter(prefix="/cart", tags=["Products"])

class CartRequest(BaseModel):
    user_id: str
    product_id: str
    quantity: int = 1

