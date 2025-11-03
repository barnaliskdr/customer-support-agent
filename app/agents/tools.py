# app/agents/tools.py
tools = [
    {
        "type": "function",
        "function": {
            "name": "list_products",
            "description": "Retrieve all available products in the store.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_product",
            "description": "Search for a product by name or keyword.",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"],
            },
        },
    },
]
