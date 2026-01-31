# PowerShell script to activate virtual environment for UV Skills project

$projectRoot = Split-Path -Parent $PSScriptRoot
$venvPath = Join-Path $projectRoot ".venv"

if (Test-Path $venvPath) {
    # Check if this is a Python virtual environment
    $activateScript = Join-Path $venvPath "Scripts\Activate.ps1"

    if (Test-Path $activateScript) {
        Write-Host "Activating virtual environment..." -ForegroundColor Green
        & $activateScript
    } else {
        Write-Host "Virtual environment found but activation script not found." -ForegroundColor Yellow
        Write-Host "Path: $venvPath" -ForegroundColor Yellow
    }
} else {
    Write-Host "Virtual environment not found at: $venvPath" -ForegroundColor Yellow
    Write-Host "To create a virtual environment, run:" -ForegroundColor Cyan
    Write-Host "  python -m venv .venv" -ForegroundColor Cyan
    Write-Host "Or install UV and run:" -ForegroundColor Cyan
    Write-Host "  uv venv" -ForegroundColor Cyan
}