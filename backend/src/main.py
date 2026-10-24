import can
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import api_router
from core.dbc import get_dbc_files
from schemas.state import StateContainer

try:
    bus = can.interface.Bus(channel="can0", bustype="socketcan")
except Exception as e:
    print(f"CAN hardware not found, using virtual bus: {e}")
    bus = can.interface.Bus(channel="vcan0", bustype="socketcan")

@asynccontextmanager
async def lifespan(app: FastAPI):
    state_container = StateContainer(bus)
    state_container.bus = bus
    state_container.data.dbc_files = get_dbc_files()
    print(state_container.data.dbc_files)
    app.state.manager = state_container
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(api_router)
app.frontend("/", directory="dist")

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
