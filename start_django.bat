@echo off
echo Starting Django server...

REM If using a virtual environment, uncomment and modify the path below
REM call venv\Scripts\activate.bat

REM Start Django server
python manage.py runserver 8000

echo Django server stopped