@echo off
REM CosmicStudio Quick Start Script for Windows

echo ==================================
echo   CosmicStudio Quick Start
echo ==================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet

echo.
echo Installation complete!
echo.
echo Starting CosmicStudio...
echo.

REM Run the application
cd src
python main.py

REM Deactivate on exit
deactivate

pause
