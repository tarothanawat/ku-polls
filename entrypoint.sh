#!/bin/sh

# Run database migrations
python manage.py migrate

# Load initial data
python manage.py loaddata data

# Create superuser if not already created
# Start the server
exec "$@"
