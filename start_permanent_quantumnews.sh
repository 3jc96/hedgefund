#!/bin/bash

echo "🌐 Starting Quantum Webscraper with Permanent URL"
echo ""

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

# Start the named tunnel
echo "🌐 Starting named tunnel with permanent URL..."
cloudflared tunnel --config cloudflare-tunnel.yml run quantum-webscraper &
TUNNEL_PID=$!
echo "✅ Named tunnel started (PID: $TUNNEL_PID)"

# Wait for tunnel to establish
echo "⏳ Waiting for tunnel to establish..."
sleep 15

echo ""
echo "🎉 Quantum Webscraper is now running!"
echo ""
echo "🌐 Your Permanent URL:"
echo "   https://quantumnews-ps23.trycloudflare.com.3jcllc.com"
echo ""
echo "📱 Mobile access: https://quantumnews-ps23.trycloudflare.com.3jcllc.com"
echo ""
echo "📊 Features:"
echo "   • Live market data (S&P 500, NASDAQ, DOW, WTI, Brent, etc.)"
echo "   • Latest financial news with sentiment analysis"
echo "   • Portfolio management"
echo "   • Mobile optimized interface"
echo ""
echo "🔧 If the permanent URL doesn't work, try the quick tunnel:"
echo "   cloudflared tunnel --url http://localhost:8081"
echo ""
echo "⏹️  To stop: pkill -f 'cloudflared tunnel' && pkill -f 'python.*start_server.py'"
