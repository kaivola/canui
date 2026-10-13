from cantools.database.can.signal import Signal
from pydantic import BaseModel
from schemas.can_message import CanMessage


class SignalDto(BaseModel):
    name: str
    comment: str | None
    length: int
    min_value: int | float | None
    max_value: int | float | None
    value: int = 0

    @classmethod
    def from_signal(cls, signal: Signal, value: int):
        return cls(
            name=signal.name,
            comment=signal.comment,
            length=signal.length,
            min_value=signal.minimum,
            max_value=signal.maximum,
            value=value
        )


class MessageDto(BaseModel):
    id: int
    signals: list[SignalDto]

    @classmethod
    def from_can_message(cls, message: CanMessage):
        return cls(
            id=message.id,
            signals=[SignalDto.from_signal(s, message.signal_values[s.name]) for s in message.dbc_entry.signals],
        )
