from fastapi import APIRouter, Depends
from schemas.dto.status_dto import StatusDto
from schemas.state import StateContainer
from schemas.status import Status
from util.get_state import get_state

router = APIRouter()


@router.get("", response_model=StatusDto)
def get_status(state: StateContainer = Depends(get_state)):
    return {"isBroadcasting": state.data.is_broadcasting}


@router.put("", response_model=StatusDto)
def update_status(data: Status, state: StateContainer = Depends(get_state)):
    if data.status == "start":
        state.data.is_broadcasting = True
        for msg in state.data.messages:
            msg.start_send_periodic(state.bus)
    elif data.status == "stop":
        state.data.is_broadcasting = False
        state.bus.stop_all_periodic_tasks()

    return {"isBroadcasting": state.data.is_broadcasting}
