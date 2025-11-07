from fastapi import APIRouter, HTTPException
from app.services import cart_service  # import the service
from app.schemas.cart_schema import CartRequest
from app.models.cart_model import Cart
from fastapi.encoders import jsonable_encoder

router = APIRouter(prefix="/cart", tags=["Products"])  # 👈 cleaner URL prefix

@router.post("/add")
def add_to_cart(request: CartRequest):
    try:
        # service already returns a Cart instance
        cart = cart_service.create_or_update_cart(request.user_id, request.product_id, request.quantity)
        return {"message": "Item added to cart successfully", "cart": jsonable_encoder(cart)}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.post("/remove")
def remove_from_cart(request: CartRequest):
    try:
        cart = cart_service.remove_from_cart(request.user_id, request.product_id, request.quantity)
        return {"message": "Item removed from cart successfully", "cart": jsonable_encoder(cart)}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.get("/getCartDetails/{user_id}")
def fetch_cart_details(user_id: str):
    try:
        cart = cart_service.fetch_cart_details(user_id)
        return {"message": "Cart details fetched successfully", "cart": jsonable_encoder(cart)}
    except ValueError as e:
        print("ValueError:", str(e))    
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        print("Exception :", str(e))    
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    


