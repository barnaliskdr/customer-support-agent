# ✅ Importing BaseModel and Field from Pydantic
# BaseModel → the foundation for data validation & serialization.
# Field → used to provide extra information like description, default values, etc.
from pydantic import BaseModel, Field

# ✅ Importing Optional and Enum
# Optional[T] means this field can either be of type T or None.
# Enum lets us define a set of allowed constant values.
from typing import Optional
from enum import Enum

# ✅ Importing PyObjectId (custom helper to handle MongoDB ObjectIds)
# This helps FastAPI & Pydantic convert MongoDB’s ObjectId (which is not JSON serializable)
# into a readable string format for API responses.
from app.utils.objectid_util import PyObjectId







# -------------------------------------------------------------
# ⚙️ Enum for Roles
# -------------------------------------------------------------
class UserRole(str, Enum):
    admin = "admin"
    customer = "customer"
    manager = "manager"


# -------------------------------------------------------------
# 🧱 Base Schema
# -------------------------------------------------------------
# ✅ Defines core user fields (common across all other schemas)
class UserBase(BaseModel):
    username: str = Field(..., description="The name of the user")  
    email: str = Field(..., description="User's email address")  
    address: str = Field(..., description="User's residential or delivery address")  
    phone: str = Field(..., description="User's contact phone number")  

    # ✅ Role field (default → 'customer')
    role: UserRole = Field(default=UserRole.customer, description="User role: admin, customer, or manager")


# -------------------------------------------------------------
# 🟢 Schema for creating a new user (Client → Server)
# -------------------------------------------------------------
# ✅ Used during registration or admin creation
class UserCreate(UserBase):
    password: str = Field(..., min_length=6, description="User's password (should be stored hashed)")  


class UserLogin(BaseModel):
    email: str = Field(..., description="User's email address")
    password: str = Field(..., min_length=6, description="User's password")

# -------------------------------------------------------------
# 🟡 Schema for updating existing user data (Client → Server)
# -------------------------------------------------------------
# ✅ Allows partial updates (all fields optional)
class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, description="Updated username")
    email: Optional[str] = Field(None, description="Updated email address")
    password: Optional[str] = Field(None, min_length=6, description="Updated password (hashed)")
    address: Optional[str] = Field(None, description="Updated address")
    phone: Optional[str] = Field(None, description="Updated phone number")
    role: Optional[UserRole] = Field(None, description="Updated role (admin, customer, or manager)")


# -------------------------------------------------------------
# 🔵 Schema for reading user data (Server → Client)
# -------------------------------------------------------------
# ✅ Used when returning user details to the frontend
class UserResponse(UserBase):
    id: Optional[PyObjectId] = Field(alias="_id")

    class Config:
        # ✅ Allows both “id” and “_id” field names to be recognized
        allow_population_by_field_name = True

        # ✅ Converts ObjectId → str when returning JSON
        json_encoders = {PyObjectId: str}

        # ✅ orm_mode=True allows reading from ORM-like or DB objects
        orm_mode = True


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse