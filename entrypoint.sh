#!/bin/sh

# Wait for the database to be ready
while ! nc -z $DB_HOST $DB_PORT; do
  echo "Waiting for the database to be ready..."
  sleep 1
done

# Apply Django migrations
python manage.py makemigrations
python manage.py migrate

# Start the application
exec "$@"
