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
]
