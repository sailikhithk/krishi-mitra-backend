from datetime import datetime

from pydantic import BaseModel


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
