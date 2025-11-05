# app/agents/tools.py
tools = [
    {
        "type": "function",
        "function": {
            "name": "list_products",
            "description": "Retrieve all available products in the store.",
            "parameters": {
                "type": "object",
                "properties": {},
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_product",
            "description": "Search for a product by name or keyword.",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_name": { "type": "string" }  # ✅ matches ProductAgent.search_product(query)
                },
                "required": ["product_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_product_by_category",
            "description": "Search for products by category.",
            "parameters": {
                "type": "object",
                "properties": {
                    "category": { "type": "string" }  # ✅ matches ProductAgent.search_product_by_category(category)
                },
                "required": ["category"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "add_to_cart",
            "description": "Add a product to a user's cart or update its quantity if already exists.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "The unique ID of the user."
                    },
                    "product_id": {
                        "type": "string",
                        "description": "The unique ID of the product to add or update."
                    },
                    "quantity": {
                        "type": "integer",
                        "description": "Number of units of the product to add."
                    }
                },
                "required": ["user_id", "product_id", "quantity"]
            }
        }
    },
    {
    "type": "function",
    "function": {
        "name": "remove_from_cart",
        "description": "Remove or decrease a product quantity from a user's cart. Deletes the cart if it becomes empty.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "The unique ID of the user."
                },
                "product_id": {
                    "type": "string",
                    "description": "The unique ID of the product to remove or decrement."
                },
                "quantity": {
                    "type": "integer",
                    "description": "Number of units to remove. If final quantity <= 0, product is removed."
                }
                },
                "required": ["user_id", "product_id", "quantity"]
            }
        }
    }
]
