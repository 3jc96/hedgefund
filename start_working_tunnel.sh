#!/bin/bash

echo "🚀 Starting Quantum Webscraper with Working Tunnel"
echo ""

# Stop any existing processes
echo "🛑 Stopping existing processes..."
pkill -f "cloudflared tunnel" 2>/dev/null
pkill -f "python.*start_server.py" 2>/dev/null
sleep 2

# Start the webscraper
echo "🌐 Starting webscraper server..."
python start_server.py &
SERVER_PID=$!
echo "✅ Server started (PID: $SERVER_PID)"

# Wait for server to be ready
echo "⏳ Waiting for server to be ready..."
sleep 5

# Test local connection
if curl -s http://localhost:5002/health >/dev/null 2>&1; then
    echo "✅ Server is responding locally"
else
    echo "❌ Server not responding locally"
    exit 1
fi

# Start tunnel
echo "🌐 Starting Cloudflare tunnel..."
cloudflared tunnel --url http://localhost:5002 &
TUNNEL_PID=$!
echo "✅ Tunnel started (PID: $TUNNEL_PID)"

# Wait for tunnel to establish
echo "⏳ Waiting for tunnel to establish..."
sleep 10

# Test common URLs
echo "🧪 Testing tunnel URLs..."
URLS=(
    "https://correspondence-font-about-peninsula.trycloudflare.com"
    "https://morning-way-joins-nov.trycloudflare.com"
    "https://quantumnews-ps23.trycloudflare.com"
    "https://quantumnews-ps23.trycloudflare.com.3jcllc.com"
)

WORKING_URL=""
for url in "${URLS[@]}"; do
    echo -n "Testing $url... "
    if curl -s "$url/health" >/dev/null 2>&1; then
        echo "✅ WORKING!"
        WORKING_URL="$url"
        break
    else
        echo "❌"
    fi
done

if [ -n "$WORKING_URL" ]; then
    echo ""
    echo "🎉 SUCCESS! Your webscraper is running!"
    echo ""
    echo "🌐 URL: $WORKING_URL"
    echo "📱 Mobile access: $WORKING_URL"
    echo ""
    echo "📊 Features:"
    echo "   • Live market data (S&P 500, NASDAQ, DOW, WTI, Brent, etc.)"
    echo "   • Latest financial news with sentiment analysis"
    echo "   • Portfolio management"
    echo "   • Mobile optimized interface"
    echo ""
    echo "⏹️  To stop: pkill -f 'cloudflared tunnel' && pkill -f 'python.*start_server.py'"
else
    echo ""
    echo "❌ No working URLs found"
    echo "🔧 Try manually: cloudflared tunnel --url http://localhost:5002"
fi















