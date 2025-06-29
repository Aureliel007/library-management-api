#!/bin/bash

echo "Initializing head..."
alembic -c /app/alembic.ini upgrade head

echo "Starting Migrations..."
alembic -c /app/alembic.ini revision --autogenerate -m "alembic_migration"

echo "Starting Upgrade head..."
alembic -c /app/alembic.ini upgrade head
sleep 2

echo "Starting FastAPI app..."
uvicorn app.main:app --host 0.0.0.0 --port 80 --reload
echo "App started..."

exec "$@"