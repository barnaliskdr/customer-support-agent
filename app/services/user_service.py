from fastapi import HTTPException, status
from app.schemas.user_schema import UserCreate, UserResponse, UserLogin  # ✅ import from schema folder
from pymongo import MongoClient
import os
from jose import JWTError, jwt
from dotenv import load_dotenv
from pymongo import MongoClient
from passlib.context import CryptContext
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# def hash_password(password: str) -> str:
#     return pwd_context.hash(password)

# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     return pwd_context.verify(plain_password, hashed_password)


# def hash_password(password: str):
#     return pwd_context.hash(password)

# # Load environment variables from the .env file
# load_dotenv()

# # Fetch MongoDB URL from the .env file
# MONGO_URL = os.getenv("MONGO_URL")

# # Create a MongoDB client
# client = MongoClient(MONGO_URL)

# # Select database and collection
# db = client["ecommerce_customer_agent"]
# users_collection = db["users"]

# # -------------------------------
# # Create a new user
# # -------------------------------
# async def create_user_service(user_data: UserCreate):
#     # ✅ Check if user already exists
#     existing_user = users_collection.find_one({"email": user_data.email})
#     if existing_user:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="User with this email already exists",
#         )

#     # ✅ Convert Pydantic model to dict
#     user_dict = user_data.model_dump()
#     user_dict["password"] = hash_password(user_dict["password"])

#     # ⚠️ Important: In production, hash the password before saving
#     # Example: user_dict["password"] = hash_password(user_dict["password"])

#     # ✅ Insert into MongoDB
#     result = users_collection.insert_one(user_dict)

#     # ✅ Fetch the inserted user and return in response model
#     created_user = users_collection.find_one({"_id": result.inserted_id})
#     print("Created User:", created_user)
#     return UserResponse(**created_user)



# # async def login_user_service(user_data: UserLogin):
# #     # ✅ Find user by email
# #     user = users_collection.find_one({"email": user_data.email})
# #     if not user:
# #         raise HTTPException(
# #             status_code=status.HTTP_404_NOT_FOUND,
# #             detail="User not found",
# #         )

# #     # ✅ Verify password
# #     if not verify_password(user_data.password, user["password"]):
# #         raise HTTPException(
# #             status_code=status.HTTP_401_UNAUTHORIZED,
# #             detail="Invalid credentials",
# #         )

# #     # ✅ Return user data excluding password
# #     return UserResponse(**user)



# async def login_user_service(user_data: UserLogin):
#     # ✅ Find user by email
#     user = users_collection.find_one({"email": user_data.email})
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="User not found",
#         )

#     # ✅ Verify password
#     if not verify_password(user_data.password, user["password"]):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid credentials",
#         )

#     # ✅ Create JWT Token
#     access_token = create_access_token(data={"sub": user["email"], "role": user.get("role", "customer")})

#     # ✅ Return token and user info
#     return {
#         "access_token": access_token,
#         "token_type": "bearer",
#         "user": UserResponse(**user)
#     }


# -------------------------------
# Load environment variables
# -------------------------------
load_dotenv()
MONGO_URL = os.getenv("MONGO_URL")
JWT_SECRET = os.getenv("JWT_SECRET", "supersecretkey")  # fallback for local dev
JWT_ALGORITHM = "HS256"

# -------------------------------
# MongoDB setup
# -------------------------------
client = MongoClient(MONGO_URL)
db = client["ecommerce_customer_agent"]
users_collection = db["users"]

# -------------------------------
# Password Hashing Setup
# -------------------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# -------------------------------
# JWT Utility Functions
# -------------------------------
def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=1)):
    """Generate a JWT token with expiration time"""
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token

# -------------------------------
# Create User Service
# -------------------------------
async def create_user_service(user_data: UserCreate):
    # ✅ Check if user already exists
    existing_user = users_collection.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )

    # ✅ Convert and hash password
    user_dict = user_data.model_dump()
    user_dict["password"] = hash_password(user_dict["password"])

    # ✅ Insert into MongoDB
    result = users_collection.insert_one(user_dict)

    # ✅ Fetch and return created user
    created_user = users_collection.find_one({"_id": result.inserted_id})
    print("Created User:", created_user)
    return UserResponse(**created_user)

# -------------------------------
# Login Service
# -------------------------------
async def login_user_service(user_data: UserLogin):
    # ✅ Find user by email
    user = users_collection.find_one({"email": user_data.email})
    print("Login Attempt User:", user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    # ✅ Verify password
    if not verify_password(user_data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    # ✅ Create JWT Token
    access_token = create_access_token(data={"sub": user["email"], "role": user.get("role", "customer")})
    
    # ✅ Return token and user info
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse(**user)
    }