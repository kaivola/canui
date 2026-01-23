from fastapi import APIRouter, Depends, Request

from util.get_state import get_state
from schemas.state import StateContainer
from schemas.status import Status

router = APIRouter()

@router.get("")
async def get_status(state: StateContainer = Depends(get_state)):
    return {"isBroadcasting": state.data.isBroadcasting}


@router.put("")
async def update_status(data: Status, state: StateContainer = Depends(get_state)):
    if data.status == "start":
        state.data.isBroadcasting = True
        state.can_broadcast_event.set()
    elif data.status == "stop":
        state.data.isBroadcasting = False
        state.can_broadcast_event.clear()
    return {"isBroadcasting": state.data.isBroadcasting}
