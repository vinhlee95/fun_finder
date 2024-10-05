#!/bin/sh

# Wait for the PostgreSQL database to be ready
echo "Waiting for PostgreSQL to be ready..."
while ! nc -z db 5432; do
  sleep 1
done
echo "PostgreSQL is ready!"

# Run database migrations using the custom configuration script
echo "Running database migrations..."
alembic upgrade head

# Check if the migrations were successful
if [ $? -eq 0 ]; then
  echo "Database migrations complete!"
  # Start the FastAPI app with Uvicorn
  echo "Starting the server..."
  exec uvicorn app:app --host 0.0.0.0 --port 8000
else
  echo "Database migrations failed!"
  exit 1
fi