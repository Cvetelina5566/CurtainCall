@echo off
echo ==========================================
echo   Starting Theater Management System...
echo ==========================================

:: 1. Спираме конфликтни PostgreSQL процеси (ако има такива)
:: (Това е опционално, но полезно, ако забравиш Task Manager-а)
:: taskkill /F /IM postgres.exe /T >nul 2>&1

:: 2. Стартиране на Backend (Django)
echo Starting Backend...
start "Django Backend" cmd /k "call venv\Scripts\activate && cd curtaincall && set USE_DOCKER=yes && set DATABASE_URL=postgres://postgres:postgres@localhost:5432/curtaincall?sslmode=disable&& uv run --active manage.py runserver"

:: 3. Стартиране на Frontend (Next.js)
echo Starting Frontend...
start "Next.js Client" cmd /k "cd next_frontend && npm run dev"

echo ==========================================
echo   System is running!
echo   Backend: http://127.0.0.1:8000
echo   Frontend: http://localhost:3000
echo ==========================================
echo Press any key to close this launcher...
pause >nul