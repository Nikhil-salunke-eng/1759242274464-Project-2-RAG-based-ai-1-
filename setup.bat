@echo off
REM RAG AI Teaching Assistant - Setup Script for Windows
REM This script helps set up the project for local development

echo 🎓 RAG AI Teaching Assistant - Setup
echo ====================================
echo.

REM Check Python version
echo Checking Python version...
python --version
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.11 or higher.
    pause
    exit /b 1
)

REM Create virtual environment
echo.
echo Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment.
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo.
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo.
echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies.
    pause
    exit /b 1
)

REM Check for embeddings file
echo.
if exist "embeddings.joblib" (
    echo ✅ Found embeddings.joblib
) else (
    echo ⚠️  Warning: embeddings.joblib not found
    echo    You'll need to run the preprocessing pipeline to generate it.
)

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo.
    echo Creating .env file from template...
    copy config.env.example .env
    echo ✅ Created .env file
    echo    Please edit .env with your configuration
) else (
    echo.
    echo ✅ .env file already exists
)

echo.
echo ====================================
echo ✅ Setup complete!
echo.
echo Next steps:
echo 1. Edit .env file with your API keys or Ollama configuration
echo 2. Activate virtual environment: venv\Scripts\activate
echo 3. Run the app: streamlit run app.py
echo.
pause

