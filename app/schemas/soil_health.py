from pydantic import BaseModel

class SoilHealthCreate(BaseModel):
    ph: float
    nitrogen: float
    phosphorus: float
    potassium: float
    organic_matter: float

class SoilHealthResponse(SoilHealthCreate):
    id: int

    class Config:
        orm_mode = True
