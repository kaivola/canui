from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from schemas.state import StateContainer
from util.get_state import get_state_ws

router = APIRouter()


@router.websocket("")
async def can_data_websocket(
    websocket: WebSocket, state: StateContainer = Depends(get_state_ws)
):
    await websocket.accept()
    messages = state.data.messages
    try:
        while True:
            data = await websocket.receive_json()
            message_id = data["messageId"]
            signal_name = data["signalName"]
            value = data["value"]

            for msg in messages:
                if msg.id != message_id:
                    continue
                if signal_name not in msg.signal_values:
                    raise RuntimeError(f"Invalid signal name: {signal_name}")

                msg.update_signal(signal=signal_name, new_value=value)
                break
    except WebSocketDisconnect:
        print("Client disconnected (page refreshed or closed)")
