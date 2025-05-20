#!/bin/sh

# Run database initialization
echo "Running database initialization..."
python -m app.start

# Start FastAPI application
echo "Starting FastAPI application..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload 