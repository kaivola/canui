from pydantic import BaseModel

class ECUState(BaseModel):
    rpm: int = 0
    tps: int = 0
    map: int = 100
    clt: int = 80
    iat: int = 65
    ethanol_content: int = 0
