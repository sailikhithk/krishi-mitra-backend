from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BidBase(BaseModel):
    user_id: int
    produce_listing_id: int
    crop: str
    quantity: float
    price: float
    status: str
    acceptance_status: Optional[str] = None
    rejection_reason: Optional[str] = None
    delivery_address: Optional[str] = None

class BidCreate(BidBase):
    pass

class BidUpdate(BaseModel):
    quantity: Optional[float] = None
    price: Optional[float] = None
    status: Optional[str] = None
    acceptance_status: Optional[str] = None
    rejection_reason: Optional[str] = None
    delivery_address: Optional[str] = None

class BidRead(BidBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class BidResponse(BidRead):
    pass