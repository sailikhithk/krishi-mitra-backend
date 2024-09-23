from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class BidBase(BaseModel):
    user_id: int
    crop: str
    quantity: float
    price: float
    status: str


class BidCreate(BidBase):
    pass


class BidUpdate(BidBase):
    pass


class BidRead(BidBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
