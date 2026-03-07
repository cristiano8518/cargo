@echo off
chcp 65001 >nul
echo ========================================
echo  Карго жобасы - ортаны дайындау
echo ========================================
cd /d "%~dp0"

if not exist "venv" (
    echo [1/5] venv құрылуда...
    py -m venv venv
    if errorlevel 1 (
        echo Қате: venv құрылмады. python-ды көреміз...
        python -m venv venv
        if errorlevel 1 (
            echo Қате: venv құрылмады. Python орнатылғанын тексеріңіз.
            pause
            exit /b 1
        )
    )
    echo venv сәтті құрылды.
) else (
    echo venv бар, өткізіп жатырмыз...
)

echo [2/5] Орта іске қосылуда...
call venv\Scripts\activate.bat

echo [3/5] Django орнатылуда...
pip install -r requirements.txt

echo [4/5] Миграция...
python manage.py makemigrations
python manage.py migrate

echo [5/5] Админ құру (логин, пароль енгізіңіз)...
python manage.py createsuperuser

echo.
echo Дайын. Серверді іске қосу үшін run.bat басыңыз.
pause
