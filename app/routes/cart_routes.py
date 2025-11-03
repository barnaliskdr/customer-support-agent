from fastapi import APIRouter, HTTPException
from app.services import cart_service  # import the service


router = APIRouter(prefix="/products", tags=["Products"])  # 👈 cleaner URL prefix

@router.post("/add")
def add_to_cart(user_id: str, product_id: str, quantity: int = 1):
    try:
        cart = create_or_update_cart(user_id, product_id, quantity)
        return {"message": "Item added to cart successfully", "cart": cart.dict(by_alias=True)}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")