@echo off
cd /d "%~dp0"

call fitbuddy-env\Scripts\activate.bat

start "" http://127.0.0.1:8000/

uvicorn app.main:app --reload