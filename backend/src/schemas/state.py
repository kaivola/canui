from can import BusABC
from pydantic import BaseModel

from .can_message import CanMessage


class AppState(BaseModel):
    isBroadcasting: bool = False
    messages: list[CanMessage] = []

    class Config:
        arbitrary_types_allowed = True


# A container for the non-Pydantic objects
class StateContainer:
    def __init__(self, bus: BusABC):
        self.bus: BusABC = bus
        self.data = AppState()
