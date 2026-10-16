from cantools.database.can.signal import Signal
from pydantic import BaseModel

class SignalDto(BaseModel):
    name: str
    comment: str | None
    length: int
    min_value: int | float | None
    max_value: int | float | None
    nominal_min: int | float | None = None
    nominal_max: int | float | None = None
    step: float = 1.0
    value: int | float = 0

    @classmethod
    def from_signal(cls, signal: Signal, value: int | float):
        return cls(
            name=signal.name,
            comment=signal.comment,
            length=signal.length,
            min_value=signal.minimum,
            max_value=signal.maximum,
            value=value
        )
