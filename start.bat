@echo off
REM IELTS Mock Exam System — Startup Script (Windows)
REM Usage: start.bat         → main server only (port 8080)
REM        start.bat speech  → main server + speech server (ports 8080, 8081)

setlocal enabledelayedexpansion

set PORT=8080
set SPEECH_PORT=8081
cd /d "%~dp0"

echo ============================================
echo   IELTS Mock Exam System
echo ============================================

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: python not found. Please install Python 3.
    pause
    exit /b 1
)

echo.
echo Starting main server at http://localhost:%PORT% ...
start "IELTS-Main-Server" cmd /c "python -m http.server %PORT%"
echo   Main server started.

if /i "%~1"=="speech" (
    echo.
    echo Starting speech recognition server at http://localhost:%SPEECH_PORT% ...
    python -c "import whisper" >nul 2>&1
    if !errorlevel! neq 0 (
        echo   WARNING: openai-whisper not installed.
        echo   Install with: pip install openai-whisper
        echo   Speech recognition will NOT work.
    ) else (
        start "IELTS-Speech-Server" cmd /c "python speech-server.py %SPEECH_PORT%"
        echo   Speech server started.
    )
)

echo.
echo ============================================
echo   Open in browser: http://localhost:%PORT%
echo ============================================
echo.
echo Close the server windows to stop, or press any key here to exit this launcher.
pause >nul
