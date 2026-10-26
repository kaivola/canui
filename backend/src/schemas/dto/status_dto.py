from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class StatusDto(BaseModel):
    is_broadcasting: bool

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
