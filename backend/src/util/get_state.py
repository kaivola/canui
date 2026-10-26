from fastapi import Request, WebSocket
from schemas.state import StateContainer


def get_state(request: Request) -> StateContainer:
    return request.app.state.manager


def get_state_ws(websocket: WebSocket) -> StateContainer:
    return websocket.app.state.manager
