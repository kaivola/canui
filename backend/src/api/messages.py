from fastapi import APIRouter, Depends
from schemas.can_message import CanMessage
from schemas.dto.message_dto import MessageDto
from schemas.state import StateContainer
from util.get_state import get_state
from util.signal_ranges import MaxxECUSensibleRanges

router = APIRouter()

def map_message(message: CanMessage) -> MessageDto:
    dto = MessageDto.from_can_message(message)
    message_ranges = MaxxECUSensibleRanges.get(message.id, {})
    
    if len(message_ranges.keys()) > 0:
        for s in dto.signals:
            signal_range = message_ranges.get(s.name, None)

            if signal_range is None:
                continue
            s.nominal_min = signal_range.get("min", 0.0)
            s.nominal_max = signal_range.get("max")
            s.step = signal_range.get("step", 1.0)
        
    return dto

@router.get("", response_model=list[MessageDto])
def get_messages(state: StateContainer = Depends(get_state)):
    return sorted([map_message(m) for m in state.data.messages], key=lambda x: x.id)

@router.get("/{message_id}")
def change_message_state(message_id: int, state: StateContainer = Depends(get_state)):
    for msg in state.data.messages:
        if msg.id == message_id:
            msg.is_enabled = not msg.is_enabled
            return
    

