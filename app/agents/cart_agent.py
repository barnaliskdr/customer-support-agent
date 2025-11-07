from app.services import cart_service



class CartAgent:
    """
    Agent responsible for managing cart-related actions.
    """

    def add_to_cart(self, user_id: str, product_id: str, quantity: int):
        """
        Add a product to a user's cart or update its quantity.
        """
        try:
            cart = cart_service.create_or_update_cart(user_id, product_id, quantity)
            return {
                "status": "success",
                "message": "Cart updated successfully.",
                "cart": cart.dict()
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    def remove_from_cart(self, user_id: str, product_id: str, quantity: int):
        """
        Remove or decrement a product from the user's cart.
        """
        try:
            result = cart_service.remove_from_cart(user_id, product_id, quantity)

            # If service returns a Cart model, convert to dict
            if hasattr(result, "dict"):
                result = result.dict(by_alias=True)

            return {
                "status": "success",
                "message": "Cart updated after removal.",
                "cart": result
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
        

    def fetch_cart_details(self, user_id: str):
        """
        Fetch cart details for a specific user.
        Equivalent to the /getCartDetails/{user_id} route.
        """
        try:
            cart = cart_service.fetch_cart_details(user_id)

            # If service returned a Pydantic Cart model, serialize it
            if hasattr(cart, "dict"):
                cart_data = cart.dict(by_alias=True)
            else:
                cart_data = cart

            return {
                "status": "success",
                "message": "Cart details fetched successfully.",
                "cart": cart_data
            }

        except ValueError as e:
            return {"status": "error", "message": str(e), "code": 404}

        except Exception as e:
            return {"status": "error", "message": f"Unexpected error: {str(e)}", "code": 500}
