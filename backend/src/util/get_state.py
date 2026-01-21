from fastapi import Request
from schemas.state import StateContainer

def get_state(request: Request) -> StateContainer:
    return request.app.state.manager