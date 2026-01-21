from pydantic import BaseModel
import asyncio

from .status import StatusOptions

class AppState(BaseModel):
    isBroadcasting: bool = False
    # Note: asyncio.Event is not a Pydantic type, 
    # so we exclude it from validation logic if needed
    class Config:
        arbitrary_types_allowed = True

# A container for the non-Pydantic objects
class StateContainer:
    def __init__(self):
        self.data = AppState()
        self.can_broadcast_event = asyncio.Event()