@echo off
echo 🚀 Setting up Email Classification API...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8+ first.
    pause
    exit /b 1
)

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv .venv

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call .venv\Scripts\activate.bat

REM Install dependencies
echo 📥 Installing dependencies...
pip install -r requirements.txt

echo ✅ Setup completed successfully!
echo.
echo 🎯 To start the API server:
echo    .venv\Scripts\activate.bat
echo    cd email_classification_module
echo    python api_backend.py
echo.
echo 🌐 API will be available at: http://localhost:5001
echo 📚 Swagger UI: http://localhost:5001/swagger
pause 