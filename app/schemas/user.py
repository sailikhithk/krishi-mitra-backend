from datetime import datetime
from enum import Enum
from typing import Dict
from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import HttpUrl


class UserRole(str, Enum):
    FARMER = "farmer"
    BUYER = "buyer"
    ADMIN = "admin"
    LOGISTICS = "logistics"


class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    phone_number: str
    address: str


class UserCreate(UserBase):
    password: str
    role: UserRole
    aadhar_card_url: HttpUrl


class FarmerProfileCreate(BaseModel):
    farm_size: float
    location: str
    soil_type: str
    irrigation_facilities: str
    crop_specialization: List[str]
    certifications: List[str]
    bank_account_details: Dict[str, str]


class BuyerProfileCreate(BaseModel):
    company_name: str
    business_type: str


class LogisticsProfileCreate(BaseModel):
    vehicle_type: str
    vehicle_number: str
    has_smartphone: bool


class UserUpdate(UserBase):
    hashed_password: Optional[str] = None
    is_active: Optional[bool] = None


class UserProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    farm_size: Optional[float] = None
    location: Optional[str] = None
    soil_type: Optional[str] = None
    irrigation_facilities: Optional[str] = None
    crop_specialization: Optional[List[str]] = None
    certifications: Optional[List[str]] = None
    bank_account_details: Optional[Dict[str, str]] = None
    company_name: Optional[str] = None
    business_type: Optional[str] = None
    vehicle_type: Optional[str] = None
    vehicle_number: Optional[str] = None
    has_smartphone: Optional[bool] = None


class UserRead(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    role: UserRole
    aadhar_card_url: HttpUrl
    farm_size: Optional[float] = None
    location: Optional[str] = None
    soil_type: Optional[str] = None
    irrigation_facilities: Optional[str] = None
    crop_specialization: Optional[List[str]] = None
    certifications: Optional[List[str]] = None
    company_name: Optional[str] = None
    business_type: Optional[str] = None
    vehicle_type: Optional[str] = None
    vehicle_number: Optional[str] = None
    has_smartphone: Optional[bool] = None

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
