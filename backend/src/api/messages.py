from fastapi import APIRouter, Depends
from schemas.dto.message_dto import MessageDto
from schemas.state import StateContainer
from util.get_state import get_state

router = APIRouter()


@router.get("", response_model=list[MessageDto])
def get_messages(state: StateContainer = Depends(get_state)):
    return sorted([MessageDto.from_can_message(m) for m in state.data.messages], key=lambda x: x.id)
