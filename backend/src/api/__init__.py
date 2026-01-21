from fastapi import APIRouter
from .status import router as status_router

api_router = APIRouter()

api_router.include_router(status_router, prefix="/status", tags=["status"])