#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Apply database migrations
python manage.py migrate &

# Load initial data
python manage.py load_districts &

# Start the main application
echo "Starting Django server..."
exec python manage.py runserver 0.0.0.0:8000