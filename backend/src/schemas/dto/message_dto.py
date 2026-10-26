from pydantic import BaseModel
from schemas.dto.signal_dto import SignalDto
from schemas.can_message import CanMessage


class MessageDto(BaseModel):
    id: int
    address: int
    name: str
    signals: list[SignalDto]

    @classmethod
    def from_can_message(cls, message: CanMessage):
        return cls(
            id=message.id,
            address=message.address,
            name=message.name,
            signals=[
                SignalDto.from_signal(s, message.signal_values[s.name])
                for s in message.dbc_entry.signals
            ],
        )
