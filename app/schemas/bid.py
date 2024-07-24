from pydantic import BaseModel

class BidCreate(BaseModel):
    crop: str
    quantity: float
    price: float
    status: str

class BidResponse(BidCreate):
    id: int

    class Config:
        orm_mode = True
