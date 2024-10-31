from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class LogisticsBase(BaseModel):
    order_number: str
    produce_listing_id: int
    from_user_id: int
    to_user_id: int
    status: str
    expected_delivery: datetime
    actual_delivery: Optional[datetime] = None
    pickup_photo_url: Optional[str] = None
    delivery_photo_url: Optional[str] = None
    has_smartphone: bool


class LogisticsCreate(LogisticsBase):
    pass


class LogisticsUpdate(BaseModel):
    status: Optional[str] = None
    actual_delivery: Optional[datetime] = None
    pickup_photo_url: Optional[str] = None
    delivery_photo_url: Optional[str] = None


class LogisticsRead(LogisticsBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class LogisticsResponse(LogisticsRead):
    pass
