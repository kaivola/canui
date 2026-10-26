from enum import Enum
from pydantic import BaseModel


class StatusOptions(str, Enum):
    start = "start"
    stop = "stop"


class Status(BaseModel):
    status: StatusOptions
