@echo off
chcp 65001 >nul
cd /d "%~dp0"

if not exist "venv" (
    echo Алдымен setup.bat орындаңыз.
    pause
    exit /b 1
)

call venv\Scripts\activate.bat
echo Сервер іске қосылуда: http://127.0.0.1:8000/
py manage.py runserver
pause
