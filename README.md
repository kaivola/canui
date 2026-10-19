# CAN Simulator

A WebUI for interacting with a CAN interface. The backend parses CAN messages from a DBC file and serves them to the frontend.

The frontend opens a WebSocket connection to send signal values to the backend, which continuously updates the data transmitted over the CAN bus.

## Development

### 1. Set Up the CAN Interface

Create a virtual CAN interface:

```bash
sudo ip link add dev vcan0 type vcan
```

Bring the interface up:
```bash
sudo ip link set up vcan0
```

You can monitor the newly added virtual CAN interface with:
```bash
candump vcan0
```

### 2. Backend Setup
Navigate to the backend directory and set up the virtual environment:
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
```

Install the dependencies
```bash
pip install -r requirements.txt
```

Start FastAPI in development mode:
```bash
fastapi dev src/main.py
```

### 3. Frontend Setup
In a separate terminal, navigate to the frontend directory and install dependencies:
```bash
cd frontend
npm install
```

Start the frontend development server:
```bash
npm run dev
```

Navigate to http://localhost:5173 with your browser and the Can Simulator should open

## TODO
- Allow uploading of dbc files instead of the MaxxECU one built in
- Allow renaming of messages from the UI
- Persist messages in a db (sqlite3)
