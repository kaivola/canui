from fastapi import APIRouter
from .status import router as status_router
from .can_data import router as can_data_router

api_router = APIRouter()

api_router.include_router(status_router, prefix="/status", tags=["status"])
api_router.include_router(can_data_router, prefix="/can-data", tags=["can-data"])