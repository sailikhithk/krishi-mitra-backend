from pydantic import BaseModel

class SoilHealthBase(BaseModel):
    ph: float
    nitrogen: float
    phosphorus: float
    potassium: float
    organic_matter: float

class SoilHealthCreate(SoilHealthBase):
    pass

class SoilHealth(SoilHealthBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True