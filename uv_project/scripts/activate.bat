@echo off
REM Batch script to activate virtual environment for UV Skills project

set "PROJECT_ROOT=%~dp0.."
set "VENV_PATH=%PROJECT_ROOT%\.venv"

if exist "%VENV_PATH%" (
    REM Check if this is a Python virtual environment
    set "ACTIVATE_SCRIPT=%VENV_PATH%\Scripts\activate.bat"

    if exist "%ACTIVATE_SCRIPT%" (
        echo Activating virtual environment...
        call "%ACTIVATE_SCRIPT%"
    ) else (
        echo Virtual environment found but activation script not found.
        echo Path: %VENV_PATH%
    )
) else (
    echo Virtual environment not found at: %VENV_PATH%
    echo To create a virtual environment, run:
    echo   python -m venv .venv
    echo Or install UV and run:
    echo   uv venv
)