from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum

class ProduceCategory(str, Enum):
    DAILY = "daily"
    WEEKLY_MONTHLY = "weekly_monthly"
    DRY_SPICES_NUTS = "dry_spices_nuts"
    GRAINS = "grains"

class ProduceListingBase(BaseModel):
    crop: str
    category: ProduceCategory
    quantity: float
    base_price: float
    minimum_bid_price: float
    govt_price: float
    end_time: datetime
    description: str
    pickup_location: str
    distance: float

class ProduceListingCreate(ProduceListingBase):
    photo_urls: str  # Comma-separated URLs

class ProduceListingUpdate(BaseModel):
    crop: Optional[str] = None
    category: Optional[ProduceCategory] = None
    quantity: Optional[float] = None
    base_price: Optional[float] = None
    minimum_bid_price: Optional[float] = None
    govt_price: Optional[float] = None
    end_time: Optional[datetime] = None
    status: Optional[str] = None
    current_bid: Optional[float] = None
    photo_urls: Optional[str] = None
    description: Optional[str] = None
    pickup_location: Optional[str] = None
    distance: Optional[float] = None

class ProduceListingRead(ProduceListingBase):
    id: int
    user_id: int
    farmer_id: int
    status: str
    current_bid: float
    photo_urls: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ProduceListingResponse(ProduceListingRead):
    pass