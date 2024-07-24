from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SchemeBase(BaseModel):
    name: str
    description: str
    eligibility: str
    benefits: str

class SchemeCreate(SchemeBase):
    pass

class SchemeUpdate(SchemeBase):
    pass

class SchemeRead(SchemeBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
