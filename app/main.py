from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.routers import user, soil_health, bidding, scheme
from app.utils.access_control import requires_role
from app.utils.auth import get_current_user

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
)

app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(soil_health.router, prefix="/soil_health", tags=["soil_health"])
app.include_router(bidding.router, prefix="/bids", tags=["bids"])
app.include_router(scheme.router, prefix="/schemes", tags=["schemes"])

@app.get("/")
async def root():
    return {"message": "Welcome to Krishi Mitra API"}

@app.get("/farmer-dashboard")
@requires_role("farmer")
async def farmer_dashboard(current_user: dict = Depends(get_current_user)):
    return {"message": f"Welcome to the farmer dashboard, {current_user.username}!"}

@app.get("/vendor-dashboard")
@requires_role("vendor")
async def vendor_dashboard(current_user: dict = Depends(get_current_user)):
    return {"message": f"Welcome to the vendor dashboard, {current_user.username}!"}

@app.get("/admin-dashboard")
@requires_role("admin")
async def admin_dashboard(current_user: dict = Depends(get_current_user)):
    return {"message": f"Welcome to the admin dashboard, {current_user.username}!"}