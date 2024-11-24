#!/bin/sh

# Exit immediately if a command fails
set -e

# Wait for the database to be ready
echo "Waiting for database..."
while ! nc -z db 5432; do
  sleep 1
done
echo "Database is ready!"

# Run migrations
echo "Running migrations..."
python manage.py migrate

# Load initial data
echo "Loading initial data..."
python manage.py loaddata data/users.json


# Start the Django development server
echo "Starting server..."
python manage.py runserver 0.0.0.0:8000
