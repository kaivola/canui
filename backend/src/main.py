import asyncio
import can

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from schemas.state import AppState, StateContainer
from api import api_router


try:
    bus = can.interface.Bus(channel='can0', bustype='socketcan')
except Exception as e:
    print(f"CAN hardware not found, using virtual bus: {e}")
    bus = can.interface.Bus(channel='vcan0', bustype='socketcan')

async def can_broadcast_loop(event: asyncio.Event, state: AppState):
    while True:
        try:
            await event.wait()
            ecu_state = state.ecu_state.__dict__
            rpm = ecu_state.get("rpm", 0)
            tps = ecu_state.get("tps", 0)
            
            msg = can.Message(
                arbitration_id=0x208,
                data=[(rpm >> 8) & 0xFF, rpm & 0xFF, tps & 0xFF, 0, 0, 0, 0, 0],
                is_extended_id=False
            )
        except Exception as e:
            print(f"ERROR in broadcast loop: {type(e).__name__}: {e}")
            # Keep the loop alive even after an error
            event.clear()
            await asyncio.sleep(1)
            continue
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
    
    task = asyncio.create_task(can_broadcast_loop(state_container.can_broadcast_event, state_container.data))
    
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