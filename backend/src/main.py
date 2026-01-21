import asyncio
import can

from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from schemas.state import StateContainer
from api import api_router


ecu_state = {
    "rpm": 0,
    "tps": 0,
    "map": 100,
    "clt": 80,
    "iat": 65,
    "eth_content": 0
}

try:
    bus = can.interface.Bus(channel='can0', bustype='socketcan')
except Exception as e:
    print(f"CAN hardware not found, using virtual bus: {e}")
    bus = can.interface.Bus(channel='vcan0', bustype='socketcan')

async def can_broadcast_loop(event: asyncio.Event):
    """Background task to send CAN messages at 50Hz (every 20ms)"""
    while True:
        await event.wait()
        rpm = ecu_state["rpm"]
        tps = ecu_state["tps"]
        
        msg = can.Message(
            arbitration_id=0x208,
            data=[(rpm >> 8) & 0xFF, rpm & 0xFF, tps & 0xFF, 0, 0, 0, 0, 0],
            is_extended_id=False
        )
        try:
            bus.send(msg)
        except Exception:
            pass
        await asyncio.sleep(1)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setup state
    state_container = StateContainer()
    app.state.manager = state_container
    
    task = asyncio.create_task(can_broadcast_loop(state_container.can_broadcast_event))
    
    yield
    task.cancel()

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

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        # Receive JSON updates from React (e.g., {"rpm": 3000})
        data = await websocket.receive_json()
        print(f"received: {data}")
        ecu_state.update(data)