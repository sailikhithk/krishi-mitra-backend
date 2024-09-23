from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class SoilHealthBase(BaseModel):
    # Add your soil health fields here
    ph: float
    nitrogen: float
    phosphorus: float
    potassium: float
    organic_matter: float

class SoilHealthCreate(SoilHealthBase):
    user_id: int

class SoilHealthUpdate(SoilHealthBase):
    # You can add additional fields for update if needed
    pass

class SoilHealthRead(SoilHealthBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
