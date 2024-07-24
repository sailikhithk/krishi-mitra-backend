from pydantic import BaseModel

class SchemeCreate(BaseModel):
    name: str
    description: str
    eligibility: str
    benefits: str

class SchemeResponse(SchemeCreate):
    id: int

    class Config:
        orm_mode = True
