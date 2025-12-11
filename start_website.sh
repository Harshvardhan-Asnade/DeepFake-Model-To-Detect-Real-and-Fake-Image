#!/bin/bash
echo "🚀 Starting DeepGuard Web Application..."

# Get the absolute path of the script directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check for venv python
if [ -f "$DIR/venv/bin/python" ]; then
    PYTHON_CMD="$DIR/venv/bin/python"
elif [ -f "$DIR/venv/bin/python3" ]; then
    PYTHON_CMD="$DIR/venv/bin/python3"
else
    echo "❌ Error: Virtual environment not found in $DIR/venv"
    echo "Please make sure you have set up the virtual environment."
    exit 1
fi

echo "Using Python: $PYTHON_CMD"

cd "$DIR/backend"
echo "Starting server..."
"$PYTHON_CMD" app.py
