#!/bin/bash

echo "🌐 Getting Working URL for Quantum Webscraper"
echo ""

# Check if server is running
echo "🔍 Checking server status..."
if curl -s http://localhost:5004/health >/dev/null 2>&1; then
    echo "✅ Server is running on port 5004"
else
    echo "❌ Server not running on port 5004"
    echo "🚀 Starting server..."
    python start_server.py &
    sleep 5
fi

# Stop any existing tunnels
echo "🛑 Stopping existing tunnels..."
pkill -f "cloudflared tunnel" 2>/dev/null
sleep 2

# Start a quick tunnel
echo "🌐 Starting quick tunnel..."
cloudflared tunnel --url http://localhost:5004 &
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
    "https://africa-operating-purposes-establishing.trycloudflare.com"
    "https://older-ivory-calculated-massage.trycloudflare.com"
    "https://observations-vacation-biz-received.trycloudflare.com"
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
    echo "🎉 SUCCESS! Your webscraper is accessible at:"
    echo "   $WORKING_URL"
    echo ""
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
    echo "🔧 Try manually: cloudflared tunnel --url http://localhost:5004"
fi















