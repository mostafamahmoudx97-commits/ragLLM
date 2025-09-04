from fastapi import APIRouter,FastAPI
import os


router = APIRouter(
    prefix="/api/v1",
)

@router.get("/Health")
async def start():
    app_name = os.getenv("APP_Name")
    app_version = os.getenv("APP_Version")
    return {
   "app_name": app_name,
   "app_version": app_version,
}