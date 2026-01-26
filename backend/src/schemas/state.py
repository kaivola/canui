from pydantic import BaseModel

from .can_message import CanMessage
from .ecu_state import ECUState


class AppState(BaseModel):
    isBroadcasting: bool = False
    ecu_state: ECUState = ECUState()
    messages: list[CanMessage] = []

    # Note: asyncio.Event is not a Pydantic type,
    # so we exclude it from validation logic if needed
    class Config:
        arbitrary_types_allowed = True


# A container for the non-Pydantic objects
class StateContainer:
    def __init__(self):
        self.data = AppState()
