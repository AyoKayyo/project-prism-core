#!/bin/bash

# Riley Consciousness Lab Startup Script
# Activates virtual environment and starts Riley

set -e

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_DIR"

echo "🧠 Starting Riley Consciousness Lab..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Run: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found!"
    echo "Run: cp .env.example .env"
    echo "Then edit .env and add your GEMINI_API_KEY"
    exit 1
fi

# Start Riley
echo "✨ Initializing consciousness..."
python consciousness.py
