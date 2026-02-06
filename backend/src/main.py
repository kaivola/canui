from contextlib import asynccontextmanager

import can
from api import api_router
from core.dbc import get_db
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from schemas.can_message import CanMessage
from schemas.state import StateContainer

try:
    bus = can.interface.Bus(channel="can0", bustype="socketcan")
except Exception as e:
    print(f"CAN hardware not found, using virtual bus: {e}")
    bus = can.interface.Bus(channel="vcan0", bustype="socketcan")


@asynccontextmanager
async def lifespan(app: FastAPI):
    state_container = StateContainer(bus)
    db = get_db("./MaxxECU_v1.3.dbc")
    if db is None:
        raise RuntimeError()
    messages = [CanMessage(msg) for msg in db.messages]

    state_container.bus = bus
    state_container.data.messages = messages
    app.state.manager = state_container
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(api_router)

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
