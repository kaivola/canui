from fastapi import APIRouter, Depends, WebSocket
from pydantic import ValidationError

from schemas.ecu_state import ECUState
from schemas.state import AppState
from util.get_state import get_state_ws

router = APIRouter()

@router.websocket("")
async def can_data_websocket(websocket: WebSocket, state: AppState = Depends(get_state_ws)):
    await websocket.accept()
    ecu_state = state.data.ecu_state
    while True:
        data = await websocket.receive_json()
        for key, value in data.items():
            if hasattr(ecu_state, key):
                try:
                    # This validates ONLY the field being set
                    setattr(ecu_state, key, value)
                except (ValidationError, ValueError) as e:
                    await websocket.send_json({"error": f"Invalid value for {key}"})
            else:
                await websocket.send_json({"error": f"Field {key} does not exist"})