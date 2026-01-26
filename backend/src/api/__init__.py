from fastapi import APIRouter

from .can_data import router as can_data_router
from .messages import router as messages_router
from .status import router as status_router

api_router = APIRouter()

api_router.include_router(status_router, prefix="/status", tags=["status"])
api_router.include_router(can_data_router, prefix="/can-data", tags=["can-data"])
api_router.include_router(messages_router, prefix="/messages", tags=["messages"])
