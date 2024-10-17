from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PaymentBase(BaseModel):
    bid_id: int
    amount: float
    upi_transaction_id: str
    status: str

class PaymentCreate(PaymentBase):
    pass

class PaymentUpdate(BaseModel):
    status: Optional[str] = None
    upi_transaction_id: Optional[str] = None

class PaymentRead(PaymentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class PaymentResponse(PaymentRead):
    pass