#!/bin/bash
echo "Starting Django server..."

# If using a virtual environment, uncomment and modify the path below
# source venv/bin/activate

# Start Django server
python manage.py runserver 8000

echo "Django server stopped"