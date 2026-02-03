@echo off
echo Running LinkedIn Watcher...

rem Execute the watcher script using the virtual environment's Python interpreter
call "%~dp0uv_project\.venv\Scripts\python.exe" "%~dp0uv_project\watcher_linkedin.py"

echo.
echo LinkedIn Watcher run complete.
pause
