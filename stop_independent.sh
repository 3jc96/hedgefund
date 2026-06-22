#!/bin/bash

# Stop script for Quantum News Webscraper

cd /Users/joelchu/quantum-webscraper

echo "🛑 Stopping Quantum News Webscraper..."

# Stop Flask app
if [ -f flask.pid ]; then
    FLASK_PID=$(cat flask.pid)
    if ps -p $FLASK_PID > /dev/null 2>&1; then
        echo "Stopping Flask app (PID: $FLASK_PID)..."
        kill $FLASK_PID
        rm flask.pid
    else
        echo "Flask app not running"
        rm flask.pid
    fi
else
    echo "No Flask PID file found"
fi

# Stop Cloudflare tunnel
if [ -f tunnel.pid ]; then
    TUNNEL_PID=$(cat tunnel.pid)
    if ps -p $TUNNEL_PID > /dev/null 2>&1; then
        echo "Stopping Cloudflare tunnel (PID: $TUNNEL_PID)..."
        kill $TUNNEL_PID
        rm tunnel.pid
    else
        echo "Cloudflare tunnel not running"
        rm tunnel.pid
    fi
else
    echo "No tunnel PID file found"
fi

# Kill any remaining processes
pkill -f "python.*app.py" 2>/dev/null
pkill -f "cloudflared.*tunnel" 2>/dev/null

echo "✅ All processes stopped"














