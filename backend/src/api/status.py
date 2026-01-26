from fastapi import APIRouter, Depends

from util.get_state import get_state
from schemas.state import StateContainer
from schemas.status import Status

router = APIRouter()

@router.get("")
def get_status(state: StateContainer = Depends(get_state)):
    return {"isBroadcasting": state.data.isBroadcasting}


@router.put("")
def update_status(data: Status, state: StateContainer = Depends(get_state)):
    if data.status == "start":
        state.data.isBroadcasting = True
        state.can_broadcast_event.set()
    elif data.status == "stop":
        state.data.isBroadcasting = False
        state.can_broadcast_event.clear()
    return {"isBroadcasting": state.data.isBroadcasting}
