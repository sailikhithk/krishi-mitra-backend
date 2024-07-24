from fastapi import FastAPI
from app.routers import soil_health, bidding, user, scheme
from app.database import engine
from app import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Krishi Mitra API")

app.include_router(soil_health.router)
app.include_router(bidding.router)
app.include_router(user.router)
app.include_router(scheme.router)

@app.get("/")
async def root():
    return {"message": "Welcome to Krishi Mitra API"}