from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    dbc_dir: str = "data"
