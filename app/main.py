from fastapi import FastAPI
from app.routers import user, soil_health, bidding, scheme

app = FastAPI()

app.include_router(user.router, prefix="/api/users")
app.include_router(soil_health.router, prefix="/api/soil_health")
app.include_router(bidding.router, prefix="/api/bidding")
app.include_router(scheme.router, prefix="/api/schemes")

@app.get("/")
async def root():
    return {"message": "Welcome to Krishi Mitra API"}
