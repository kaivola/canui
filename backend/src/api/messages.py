from fastapi import APIRouter, Depends, HTTPException
from schemas.metadata import SignalMetadata
from core.dbc import get_metadata, read_dbc_file
from schemas.can_message import CanMessage
from schemas.dto.message_dto import MessageDto
from schemas.state import StateContainer
from util.get_state import get_state

router = APIRouter()

def map_message(message: CanMessage, metadata: dict[str, SignalMetadata] | None) -> MessageDto:
    dto = MessageDto.from_can_message(message)
    if metadata is None:
        return dto
    
    if len(metadata.keys()) > 0:
        for s in dto.signals:
            signal_metadata = metadata.get(s.name, None)

            if signal_metadata is None:
                continue

            s.nominal_min = signal_metadata.min
            s.nominal_max = signal_metadata.max
            s.step = signal_metadata.step
            s.display_name = signal_metadata.displayName
        
    return dto

@router.get("/dbc-files", response_model=list[str])
def get_dbc_files(state: StateContainer = Depends(get_state)):
    return state.data.dbc_files

@router.post("/dbc-files/{filename}", response_model=list[MessageDto])
def select_dbc_file(filename: str, state: StateContainer = Depends(get_state)):
    db = read_dbc_file(filename)
    if db is None:
        raise HTTPException(status_code=400, detail="Invalid file")
    messages = [CanMessage(msg) for msg in db.messages]
    state.data.messages = messages
    metadata = get_metadata(filename)

    return sorted([map_message(msg, metadata.root.get(msg.id) if metadata is not None else None) for msg in messages], key=lambda x: x.id)

@router.post("/{message_id}/enable")
def enable_message(message_id: int, state: StateContainer = Depends(get_state)):
    for msg in state.data.messages:
        if msg.id == message_id:
            msg.is_enabled = True
            return

@router.post("/{message_id}/disable")
def disable_message(message_id: int, state: StateContainer = Depends(get_state)):
    for msg in state.data.messages:
        if msg.id == message_id:
            msg.is_enabled = False
            return
