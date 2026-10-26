# Build the frontend
FROM node:20-alpine AS frontend
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build


# Setup backend
FROM python:3.11-slim AS backend-builder
WORKDIR /app

COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r backend/requirements.txt

COPY backend/ ./backend/

# Copy frontend files into the backend's dist dir
COPY --from=frontend /app/frontend/dist ./backend/dist


FROM python:3.11-slim
WORKDIR /app

COPY --from=backend-builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=backend-builder /usr/local/bin /usr/local/bin
COPY --from=backend-builder /app/backend ./backend

EXPOSE 8000
WORKDIR /app/backend

CMD ["fastapi", "run", "src/main.py", "--port", "8000"]