from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SoilHealthBase(BaseModel):
    user_id: int
    ph: float
    nitrogen: float
    phosphorus: float
    potassium: float
    organic_matter: float

class SoilHealthCreate(SoilHealthBase):
    pass

class SoilHealthUpdate(SoilHealthBase):
    pass

class SoilHealthRead(SoilHealthBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
