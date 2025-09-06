from fastapi import APIRouter,FastAPI,Depends
import os
from helpers.config import get_settings ,Settings

base_router = APIRouter(
    prefix="/api/v1",
)

@base_router.get("/Health")
async def start(app_setting: Settings =Depends(get_settings)):
    
    app_name = app_setting.APP_Name
    app_version = app_setting.APP_Version

    return {
   "app_name": app_name,
   "app_version": app_version
}