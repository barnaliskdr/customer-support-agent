from fastapi import APIRouter, HTTPException
from app.services import cart_service  # import the service
from app.schemas.cart_schema import CartRequest
from app.models.cart_model import Cart
from fastapi.encoders import jsonable_encoder

router = APIRouter(prefix="/cart", tags=["Products"])  # 👈 cleaner URL prefix

# @router.post("/add")
# def add_to_cart(user_id: str, product_id: str, quantity: int):
#     try:
#         cart = cart_service.create_or_update_cart(user_id, product_id, quantity)
#         return {"message": "Item added to cart successfully", "cart": cart.dict(by_alias=True)}
#     except ValueError as e:
#         raise HTTPException(status_code=404, detail=str(e))
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# @router.post("/add")
# def add_to_cart(request: CartRequest):
#     print("Cart after addition:", request)
#     try:
#         cart = cart_service.create_or_update_cart(
#             request.user_id, request.product_id, request.quantity
#         )
        
#         return {"message": "Item added to cart successfully", "cart": cart.dict(by_alias=True)}
#     except ValueError as e:
#         raise HTTPException(status_code=404, detail=str(e))
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# @router.post("/add")
# def add_to_cart(request: CartRequest):
#     try:
#         cart_data = cart_service.create_or_update_cart(request.user_id, request.product_id, request.quantity)
#         cart = Cart(cart_data)  # Convert MongoDB dict → Pydantic model
#         return {"message": "Item added to cart successfully", "cart": jsonable_encoder(cart)}
#     except ValueError as e:
#         raise HTTPException(status_code=404, detail=str(e))
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


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