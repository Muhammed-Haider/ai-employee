#!/bin/bash
# Shell script to activate virtual environment for UV Skills project

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_PATH="$PROJECT_ROOT/.venv"

if [ -d "$VENV_PATH" ]; then
    # Check if this is a Python virtual environment
    ACTIVATE_SCRIPT="$VENV_PATH/bin/activate"

    if [ -f "$ACTIVATE_SCRIPT" ]; then
        echo "Activating virtual environment..."
        source "$ACTIVATE_SCRIPT"
    else
        echo "Virtual environment found but activation script not found."
        echo "Path: $VENV_PATH"
    fi
else
    echo "Virtual environment not found at: $VENV_PATH"
    echo "To create a virtual environment, run:"
    echo "  python -m venv .venv"
    echo "Or install UV and run:"
    echo "  uv venv"
fi