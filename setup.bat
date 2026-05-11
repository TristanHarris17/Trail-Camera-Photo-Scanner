@echo off
echo ===========================================
echo Setting up Trail Camera Photo Scanner...
echo ===========================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not added to your PATH.
    echo Please install Python 3 from https://www.python.org/downloads/ 
    echo IMPORTANT: Make sure to check the box "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

echo Creating virtual environment (venv)...
python -m venv venv

echo.
echo Activating virtual environment and installing dependencies...
echo This may take a few minutes depending on your internet connection...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo Downloading AI Model for offline use...
python download_model.py

echo.
echo ===========================================
echo Setup Complete!
echo ===========================================
echo.
echo To run the scanner in the future:
echo 1. Open Command Prompt or PowerShell in this folder
echo 2. Type: call venv\Scripts\activate.bat
echo 3. Type: python scanner.py
echo.
pause
