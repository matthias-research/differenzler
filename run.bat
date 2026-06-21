@echo off
cd /d "%~dp0"

python -m ui.pygame_app
if errorlevel 1 (
    echo.
    echo Failed to start. Install dependencies with:
    echo   pip install -e ".[ui]"
    pause
)
