# app/agents/product_agent.py
from typing import List, Dict, Any
# from app.services.product_service import ProductService
from app.services import product_service
from app.models.product_model import Product


class ProductAgent:
    """Agent that handles all product-related operations."""

    name = "product_agent"
    description = "Handles queries related to product listing and searching."

    # def __init__(self):
    #     self.service = ProductService()


    def list_products(self) -> List[Dict[str, Any]]:
        """Return all products available in the catalog."""
        products = product_service.get_all_products()
        return [self._serialize_product(p) for p in products]

    def search_product(self, product_name: str) -> List[Dict[str, Any]]:
        """Search products by partial name match."""
        products = product_service.get_product_by_name(product_name)
        return [self._serialize_product(p.dict() if isinstance(p, Product) else p) for p in products]

    def search_product_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Search products by category."""
        products = product_service.get_product_by_category(category)
        return [self._serialize_product(p.dict() if isinstance(p, Product) else p) for p in products]
    
    def _serialize_product(self, product: Dict[str, Any]) -> Dict[str, Any]:
        product["_id"] = str(product.get("_id", ""))
        return product

    # def list_products(self):
    #     """Tool: list_products — Fetch all available products."""
    #     products = self.service.get_all_products()
    #     return {"products": products}

    # def search_product(self, query: str):
    #     """Tool: search_product — Search product by name."""
    #     products = self.service.search_products(query)
    #     return {"products": products}