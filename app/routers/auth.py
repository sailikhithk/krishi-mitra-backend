from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import user as user_crud
from app.schemas.user import UserCreate
from app.utils.auth import create_access_token, verify_password, authenticate_user
from app.dependencies import get_db
from pydantic import BaseModel
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter()

class Token(BaseModel):
    access_token: str
    token_type: str

class ResetPasswordRequest(BaseModel):
    email: str

class ResetPasswordConfirm(BaseModel):
    token: str
    new_password: str

class VerifyPasswordRequest(BaseModel):
    username: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/reset-password-request", response_model=dict)
async def reset_password_request(request: ResetPasswordRequest, db: AsyncSession = Depends(get_db)):
    user = await user_crud.get_user_by_email(db, email=request.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    token = await user_crud.set_password_reset_token(db, user.id)
    # In a real-world scenario, you would send this token via email
    return {"message": "Password reset token generated", "token": token}

@router.post("/reset-password-confirm", response_model=dict)
async def reset_password_confirm(request: ResetPasswordConfirm, db: AsyncSession = Depends(get_db)):
    success = await user_crud.reset_password(db, request.token, request.new_password)
    if not success:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    return {"message": "Password reset successful"}

@router.post("/verify-password", response_model=dict)
async def verify_user_password(request: VerifyPasswordRequest, db: AsyncSession = Depends(get_db)):
    user = await user_crud.get_user_by_username(db, username=request.username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    is_password_correct = verify_password(request.password, user.hashed_password)
    
    return {
        "username": user.username,
        "password_verified": is_password_correct
    }

@router.post("/login")
async def login(login_data: LoginRequest, db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db, login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register")
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    logger.debug(f"Attempting to register user: {user.username}")
    db_user = await user_crud.get_user_by_username(db, username=user.username)
    if db_user:
        logger.warning(f"User already exists: {user.username}")
        raise HTTPException(status_code=400, detail="Username already registered")
    try:
        new_user = await user_crud.create_user(db, user)
        logger.info(f"User registered successfully: {new_user.username}")
        return new_user
    except Exception as e:
        logger.error(f"Error registering user: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# ... existing login and registration endpoints ...