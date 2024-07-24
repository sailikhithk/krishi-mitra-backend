from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db

router = APIRouter(
    prefix="/soil-health",
    tags=["soil health"]
)

@router.post("/", response_model=schemas.SoilHealth)
def create_soil_health(soil_health: schemas.SoilHealthCreate, db: Session = Depends(get_db)):
    return crud.soil_health.create_soil_health(db=db, soil_health=soil_health)

@router.get("/{soil_health_id}", response_model=schemas.SoilHealth)
def read_soil_health(soil_health_id: int, db: Session = Depends(get_db)):
    db_soil_health = crud.soil_health.get_soil_health(db, soil_health_id=soil_health_id)
    if db_soil_health is None:
        raise HTTPException(status_code=404, detail="Soil health record not found")
    return db_soil_health