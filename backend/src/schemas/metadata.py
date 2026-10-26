from pydantic import BaseModel, RootModel


class SignalMetadata(BaseModel):
    displayName: str | None = None
    min: int | float | None = None
    max: int | float | None = None
    step: float | int = 1.0


class Metadata(RootModel[dict[int, dict[str, SignalMetadata]]]):
    pass
