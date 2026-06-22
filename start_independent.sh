#!/bin/bash

# Independent startup script for Quantum News Webscraper
# This runs in the background and persists even when Cursor is closed

cd /Users/joelchu/quantum-webscraper

# Kill any existing processes
echo "🔄 Stopping existing processes..."
pkill -f "python.*app.py" 2>/dev/null
pkill -f "cloudflared.*tunnel" 2>/dev/null
sleep 2

# Start Flask app on port 8081 (avoiding port 5000 conflict with macOS AirPlay)
echo "🚀 Starting Flask app on port 8081..."
PORT=8081 nohup python3 app.py > flask.log 2>&1 &
FLASK_PID=$!
echo "Flask PID: $FLASK_PID"

# Wait for Flask to start
sleep 3

# Check if Flask is running
if curl -s http://localhost:8081/qa > /dev/null; then
    echo "✅ Flask app started successfully on port 8081"
else
    echo "❌ Flask app failed to start"
    exit 1
fi

# Start Cloudflare tunnel
echo "🌐 Starting Cloudflare tunnel..."
nohup cloudflared tunnel --config cloudflare-tunnel.yml run > tunnel.log 2>&1 &
TUNNEL_PID=$!
echo "Tunnel PID: $TUNNEL_PID"

# Wait for tunnel to connect
sleep 5

# Test the public URL
if curl -s https://quantumnews-ps23.3jcllc.com/qa > /dev/null; then
    echo "✅ Cloudflare tunnel connected successfully"
    echo "🌍 Public URL: https://quantumnews-ps23.3jcllc.com"
    echo "🏠 Local URL: http://localhost:8081"
else
    echo "⚠️  Cloudflare tunnel may still be connecting..."
fi

# Save PIDs for easy stopping
echo "$FLASK_PID" > flask.pid
echo "$TUNNEL_PID" > tunnel.pid

echo "📝 Logs:"
echo "   Flask: $(pwd)/flask.log"
echo "   Tunnel: $(pwd)/tunnel.log"
echo ""
echo "🛑 To stop: ./stop_independent.sh"
echo "📊 To check status: ./status_independent.sh"
