# Import the BaseModel class from Pydantic
# Pydantic is used for data validation — it ensures that any data
# coming into (or going out of) your API matches the schema you define.
from pydantic import BaseModel, Field

# Import Optional from typing module.
# Optional means this field is not mandatory — it can be missing or None.
from typing import Optional

# ObjectId is the unique identifier MongoDB uses for each document (like primary key).
from bson import ObjectId

# Import a custom utility we’ll use to convert MongoDB ObjectId <-> string
# because FastAPI/Pydantic doesn't understand ObjectId by default.
from utils.objectid_util import PyObjectId


# -------------------------------------------------------------------------
# BASE SCHEMA (shared by all operations like Create, Update, Read)
# -------------------------------------------------------------------------
class ProductBase(BaseModel):
    # Each product has a 'name' (required)
    # Field(...) → means it's required (the three dots "..." are Pydantic’s required marker)
    # description → helps automatically document the API (shows up in Swagger UI)
    name: str = Field(..., description="Name of the product")

    # Product category (required)
    category: str = Field(..., description="Product category")

    # Product price (required)
    # gt=0 → ensures the price must be greater than 0 (validation rule)
    price: float = Field(..., gt=0, description="Price of the product")

    # Portion or variant (required)
    portion: str = Field(..., description="Portion size or variant")

    # Image URL (required)
    image: str = Field(..., description="Image URL of the product")

    # Description (required)
    description: str = Field(..., description="Detailed description of the product")


# -------------------------------------------------------------------------
# SCHEMA FOR PRODUCT CREATION (used when client sends POST request)
# -------------------------------------------------------------------------
# Inherits all the fields from ProductBase
# No new fields or changes — just a clearer separation of responsibility.
class ProductCreate(ProductBase):
    pass  # Means "no extra code here", but class exists for clarity


# -------------------------------------------------------------------------
# SCHEMA FOR PRODUCT UPDATES (PATCH or PUT requests)
# -------------------------------------------------------------------------
# When updating, we don't require all fields — any can be optional.
# For example, the user might just update 'price' or 'image'.
# class ProductUpdate(BaseModel):
#     name: Optional[str] = None
#     category: Optional[str] = None
#     price: Optional[float] = None
#     portion: Optional[str] = None
#     image: Optional[str] = None
#     description: Optional[str] = None


# -------------------------------------------------------------------------
# SCHEMA FOR RESPONSE DATA (when sending data back to client)
# -------------------------------------------------------------------------
class ProductResponse(ProductBase):
    # MongoDB automatically generates an _id field for each document.
    # We alias it to "id" in Python, so we can use it like product.id
    # but when it goes to the database, it maps to "_id".
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")

    # Config class inside Pydantic defines extra behaviors for the model
    class Config:
        # allow_population_by_field_name=True
        # Means you can pass either "id" or "_id" when creating this object.
        # e.g. ProductResponse(_id="123") or ProductResponse(id="123") — both work.
        allow_population_by_field_name = True

        # json_encoders
        # Tells Pydantic how to convert special types (like ObjectId) to JSON strings.
        # ObjectId is not natively JSON serializable, so we convert it to str.
        json_encoders = {ObjectId: str}

        # orm_mode = True
        # Allows Pydantic to work with ORM objects (like those returned by Mongo or SQLAlchemy)
        # It lets you create a schema from model objects (not just dicts).
        orm_mode = True
