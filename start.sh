#!/bin/bash
echo "Running migrations..."
python manage.py migrate --noinput || true

echo "Creating default admin..."
python manage.py create_admin || true

echo "Starting Gunicorn..."
gunicorn nutri_project.wsgi:application --bind 0.0.0.0:$PORT
