@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ========================================
echo  venv құру
echo ========================================
echo.

echo [1] Python тексеру...
python --version
if errorlevel 1 (
    echo python жұмыс істемейді, py-ны көреміз...
    py --version
    if errorlevel 1 (
        echo Қате: Python табылмады. Python орнатыңыз: https://www.python.org/downloads/
        pause
        exit /b 1
    )
    echo py командасы бар, оны қолданамыз.
    set PYTHON_CMD=py
) else (
    echo python командасы бар.
    set PYTHON_CMD=python
)

echo.
echo [2] venv құру...
if exist "venv" (
    echo venv бар, жою...
    rmdir /s /q venv
)

%PYTHON_CMD% -m venv venv

if errorlevel 1 (
    echo Қате: venv құрылмады.
    pause
    exit /b 1
)

if exist "venv\Scripts\activate.bat" (
    echo venv сәтті құрылды!
    echo.
    echo Келесі қадам: setup.bat орындаңыз
) else (
    echo venv құрылды, бірақ activate.bat табылмады. venv папкасын тексеріңіз.
    dir venv
)

echo.
pause
