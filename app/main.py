from fastapi import FastAPI
from app.routers import user, soil_health, bidding, scheme

app = FastAPI(
    title="Krishi Mitra API",
    description="API documentation for the Krishi Mitra application.",
    version="1.0.0",
)

app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(soil_health.router, prefix="/soil_health", tags=["soil_health"])
app.include_router(bidding.router, prefix="/bids", tags=["bids"])
app.include_router(scheme.router, prefix="/schemes", tags=["schemes"])

@app.get("/")
async def root():
    return {"message": "Welcome to Krishi Mitra API"}
