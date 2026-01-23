from pydantic import BaseModel
import asyncio

from .ecu_state import ECUState

class AppState(BaseModel):
    isBroadcasting: bool = False
    ecu_state: ECUState = ECUState()
    # Note: asyncio.Event is not a Pydantic type, 
    # so we exclude it from validation logic if needed
    class Config:
        arbitrary_types_allowed = True

# A container for the non-Pydantic objects
class StateContainer:
    def __init__(self):
        self.data = AppState()
        self.can_broadcast_event = asyncio.Event()