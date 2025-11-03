from fastapi import APIRouter,  HTTPException
from app.schemas.user_schema import UserCreate, UserResponse, UserLogin, LoginResponse
from app.services.user_service import create_user_service, login_user_service
router = APIRouter(prefix="/users", tags=["Users"])


# -------------------------------------------------------------
# Route: Create a new user
# -------------------------------------------------------------
@router.post("/createuser")
async def add_user(user: UserCreate):
    try:
        await create_user_service(user)
        return {"message": "User registered successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/login",  response_model=LoginResponse)
async def login_user(user_data: UserLogin):
    try:
        result = await login_user_service(user_data)
        print("Login Result:", result)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))