#!/bin/bash

# Quantum Webscraper Startup Script
echo "🚀 Starting Quantum News Webscraper..."

# Function to find available port
find_available_port() {
    local port=5000
    while lsof -i :$port >/dev/null 2>&1; do
        echo "Port $port is in use, trying next port..."
        port=$((port + 1))
    done
    echo $port
}

# Find available port
PORT=$(find_available_port)
echo "✅ Using port $PORT"

# Set environment variable and start server
export PORT=$PORT
python app.py


