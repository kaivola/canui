from cantools.database.can.signal import Signal
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

class SignalDto(BaseModel):
    name: str
    comment: str | None
    length: int
    min_value: int | float | None
    max_value: int | float | None
    display_name: str | None = None
    nominal_min: int | float | None = None
    nominal_max: int | float | None = None
    step: float = 1.0
    value: int | float = 0

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True
    )

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
