from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    FARMER = "farmer"
    BUYER = "buyer"
    ADMIN = "admin"

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: UserRole
    phone_number: str

class UserUpdate(UserBase):
    hashed_password: Optional[str] = None
    is_active: Optional[bool] = None

class UserProfileUpdate(BaseModel):
    phone_number: Optional[str] = None
    farm_size: Optional[float] = None
    location: Optional[str] = None
    company_name: Optional[str] = None
    business_type: Optional[str] = None

class UserRead(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    role: UserRole
    phone_number: str
    farm_size: Optional[float] = None
    location: Optional[str] = None
    company_name: Optional[str] = None
    business_type: Optional[str] = None

    class Config:
        from_attributes = True

class UserResponse(UserRead):
    pass

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[UserRole] = None