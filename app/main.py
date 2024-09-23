"""
Main entry point for the FastAPI application.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import bidding, scheme, soil_health, user, auth
from app.database import engine, Base
from app.models import user as user_model, soil_health as soil_health_model, bid as bid_model, scheme as scheme_model, weather_data as weather_data_model, market_price as market_price_model

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Krishi Mitra API",
    description="API documentation for the Krishi Mitra application.",
    version="1.0.0",
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    logger.info("Starting up the application")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created")

app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(soil_health.router, prefix="/soil_health", tags=["soil_health"])
app.include_router(bidding.router, prefix="/bidding", tags=["bidding"])
app.include_router(scheme.router, prefix="/schemes", tags=["schemes"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])

@app.get("/")
async def root():
    return {"message": "Welcome to Krishi Mitra API"}
