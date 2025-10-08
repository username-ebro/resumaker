#!/bin/bash
# Startup script for Railway deployment
# Ensures PORT variable is properly set and passed to uvicorn

# Use Railway's PORT or default to 8000
export PORT=${PORT:-8000}

# Start uvicorn with the PORT variable
exec uvicorn main:app --host 0.0.0.0 --port "$PORT"
