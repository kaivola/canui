# CAN simulator

### Developing
Add virtual can interface with

`sudo ip link add dev vcan0 type vcan`

Set it up

`sudo ip link set up vcan0`

Activate virtual env for the backend

`source ./backend/.venv/bin/activate`

Install dependencies

`pip install -r ./backend/requirements.txt`

Start FastAPI in dev mode

`fastapi dev ./backend/src/main.py`