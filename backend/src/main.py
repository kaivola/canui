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

async def can_broadcast_loop(event: asyncio.Event, state: AppState, freq: int):
    msg = can.Message(
        arbitration_id=0x208 * freq,
        data=[(freq >> 8) & 0xFF, freq & 0xFF, freq & 0xFF, 0, 0, 0, 0, 0],
        is_extended_id=False
    )
    period = 1.0 / freq
    task = bus.send_periodic(msg, period=period, autostart=False)
    last_sent_data = msg
    while True:
        await event.wait()
        task.start()
        while state.isBroadcasting:
            try:
                # rpm = state.ecu_state.get("rpm", 0)
                # tps = state.ecu_state.get("tps", 0)
                
                current_data = list(state.ecu_state.rpm.to_bytes(2, 'big')) + [0]*6
                print(f"prev: {last_sent_data} - curr: {current_data}")
                if current_data != last_sent_data:
                    task.modify_data(can.Message(
                        arbitration_id=0x208 * freq, 
                        data=current_data
                    ))
                last_sent_data = current_data

            except Exception as e:
                print(f"ERROR in broadcast loop: {type(e).__name__}: {e}")
                # Keep the loop alive even after an error
                event.clear()
                await asyncio.sleep(1)
                continue
            await asyncio.sleep(0.1)
        task.stop()
        event.clear()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setup state
    state_container = StateContainer()
    app.state.manager = state_container
    
    can_broadcast_task_10hz = asyncio.create_task(can_broadcast_loop(state_container.can_broadcast_event, state_container.data, 10))
    can_broadcast_task_20hz = asyncio.create_task(can_broadcast_loop(state_container.can_broadcast_event, state_container.data, 20))
    can_broadcast_task_50hz = asyncio.create_task(can_broadcast_loop(state_container.can_broadcast_event, state_container.data, 50))
    
    yield
    can_broadcast_task_10hz.cancel()
    can_broadcast_task_20hz.cancel()
    can_broadcast_task_50hz.cancel()

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