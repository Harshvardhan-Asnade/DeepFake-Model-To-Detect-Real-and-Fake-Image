@echo off
REM DeepGuard Web Application Launcher

echo ================================================
echo DeepGuard - Deepfake Detection Web Application
echo ================================================
echo.

REM Check if model exists
if exist "..\model\checkpoints\best_model.keras" (
    echo [OK] Model found!
    echo.
) else (
    echo [WARNING] Model not found at ..\model\checkpoints\best_model.keras
    echo.
    echo Please train the model first by running:
    echo   cd ..\model ^& python main.py --epochs 10 --batch-size 32
    echo.
    echo Would you like to continue anyway? (The app will warn about missing model)
    pause
    echo.
)

echo Starting web server...
echo.
echo Once started, open your browser to:
echo   http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo ================================================
echo.

python app.py

pause
