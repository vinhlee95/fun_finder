#!/bin/bash

# Step 1: Truncate the available_slots table in the tennis_reservation database
echo "Truncating available_slots table..."
psql -U vinhle -d tennis_reservation -c "TRUNCATE TABLE available_slot;"

# Step 2: Run the Python script to refetch available slots
echo "Running Python script to refetch available slots..."
export PYTHONPATH="${PYTHONPATH}:/path/to/your/project"
python jobs/main.py

echo "Done."