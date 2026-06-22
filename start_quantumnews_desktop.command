#!/bin/bash

# Quantum News PS23 - Desktop Startup Script
# Double-click this file to start your webscraper

echo "🚀 Starting Quantum News PS23..."
echo ""

# Navigate to the project directory
cd /Users/joelchu/quantum-webscraper

# Stop any existing processes
echo "🛑 Stopping existing processes..."
pkill -f "cloudflared tunnel" 2>/dev/null
pkill -f "python.*start_server.py" 2>/dev/null
pkill -f "python.*app.py" 2>/dev/null
sleep 3

# Start the webscraper
echo "🌐 Starting webscraper server..."
python start_server.py &
SERVER_PID=$!
echo "✅ Server started (PID: $SERVER_PID)"

# Wait for server to be ready
echo "⏳ Waiting for server to be ready..."
sleep 5

# Test local connection
if curl -s http://localhost:8081/health >/dev/null 2>&1; then
    echo "✅ Server is responding locally on port 8081"
else
    echo "❌ Server not responding locally"
    exit 1
fi

# Start Cloudflare tunnel
echo "🌐 Starting Cloudflare tunnel..."
cloudflared tunnel --config cloudflare-tunnel.yml run quantum-webscraper &
TUNNEL_PID=$!
echo "✅ Tunnel started (PID: $TUNNEL_PID)"

# Wait for tunnel to establish
echo "⏳ Waiting for tunnel to establish..."
sleep 10

echo ""
echo "🎉 Quantum News PS23 is ready!"
echo ""
echo "🌐 Your webscraper:"
echo "   https://quantumnews-ps23.3jcllc.com"
echo ""
echo "📱 Mobile access: https://quantumnews-ps23.3jcllc.com"
echo ""
echo "📊 Features:"
echo "   • Live market data (S&P 500, NASDAQ, DOW, WTI, VIX)"
echo "   • Latest financial news with sentiment analysis"
echo "   • Portfolio management"
echo "   • Mobile optimized interface"
echo ""
echo "⏹️  To stop: Close this terminal or press Ctrl+C"
echo ""

# Keep the script running
wait















