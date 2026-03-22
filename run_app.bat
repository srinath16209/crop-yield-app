@echo off
REM Change directory to your project folder
cd /d "C:\Main Project"

REM Activate your virtual environment
call .venv\Scripts\activate

REM Run your Flask app
python app.py
