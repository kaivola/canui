from fastapi import APIRouter, Depends
from schemas.state import StateContainer
from schemas.status import Status
from util.get_state import get_state

router = APIRouter()


@router.get("")
def get_status(state: StateContainer = Depends(get_state)):
    return {"isBroadcasting": state.data.isBroadcasting}


@router.put("")
def update_status(data: Status, state: StateContainer = Depends(get_state)):
    if data.status == "start":
        state.data.isBroadcasting = True
        for msg in state.data.messages:
            msg.start_send_periodic(state.bus)
    elif data.status == "stop":
        state.data.isBroadcasting = False
        for msg in state.data.messages:
            if msg.task is None:
                raise RuntimeError()
            msg.task.stop()
    return {"isBroadcasting": state.data.isBroadcasting}
