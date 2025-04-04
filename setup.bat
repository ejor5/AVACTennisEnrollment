@echo off
echo Tennis Registration Tool Setup
echo ============================

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed! Please install Python 3.8 or higher.
    echo You can download Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit
)

:: Check if pip is installed
pip --version >nul 2>&1
if errorlevel 1 (
    echo pip is not installed! Please install pip.
    pause
    exit
)

:: Remove existing venv if it exists
if exist "venv" (
    echo Removing existing virtual environment...
    rmdir /s /q venv
)

:: Create new virtual environment
echo Creating virtual environment...
python -m venv venv --clear

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

:: Upgrade pip in virtual environment
echo Upgrading pip...
python -m pip install --upgrade pip

:: Install requirements
echo Installing required packages...
pip install -r requirements.txt

:: Check if .env file exists
if not exist ".env" (
    echo Creating .env file...
    echo Please enter your AVAC credentials:
    set /p username="Username: "
    set /p password="Password: "
    
    :: Create .env file with proper line endings
    (
        echo AVAC_USERNAME=%username%
        echo AVAC_PASSWORD=%password%
    ) > .env
    
    :: Verify the file was created
    if exist ".env" (
        echo Credentials saved successfully!
    ) else (
        echo Error: Failed to create .env file
        echo Please try running setup.bat as administrator
        pause
        exit
    )
)

:: Run the main script with full path to Python
echo.
echo Starting Tennis Registration Tool...
echo.
call venv\Scripts\python.exe main.py

:: Keep the window open if there's an error
pause 