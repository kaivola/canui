from pydantic import BaseModel
from schemas.dto.signal_dto import SignalDto
from schemas.can_message import CanMessage

class MessageDto(BaseModel):
    id: int
    signals: list[SignalDto]

    @classmethod
    def from_can_message(cls, message: CanMessage):
        return cls(
            id=message.id,
            signals=[SignalDto.from_signal(s, message.signal_values[s.name]) for s in message.dbc_entry.signals],
        )
