from fastapi import APIRouter, Request

from schemas.state import StateContainer
from schemas.status import Status

router = APIRouter()

@router.get("/")
async def get_status(request: Request):
    app_state: StateContainer = request.app.state.manager
    return {"isBroadcasting": app_state.data.isBroadcasting}


@router.put("/")
async def update_status(request: Request, data: Status):
    app_state: StateContainer = request.app.state.manager
    if data.status == "start":
        app_state.data.isBroadcasting = True
        app_state.can_broadcast_event.set()
    elif data.status == "stop":
        app_state.data.isBroadcasting = False
        app_state.can_broadcast_event.clear()
    return {"isBroadcasting": app_state.data.isBroadcasting}
