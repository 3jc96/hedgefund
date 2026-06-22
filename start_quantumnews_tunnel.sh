#!/bin/bash

echo "🌐 Starting Quantum News Webscraper with Consistent URL"
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
if curl -s http://localhost:5004/health >/dev/null 2>&1; then
    echo "✅ Server is responding locally on port 5004"
else
    echo "❌ Server not responding locally"
    exit 1
fi

# Start tunnel
echo "🌐 Starting Cloudflare tunnel..."
cloudflared tunnel --url http://localhost:5004 &
TUNNEL_PID=$!
echo "✅ Tunnel started (PID: $TUNNEL_PID)"

# Wait for tunnel to establish
echo "⏳ Waiting for tunnel to establish..."
sleep 10

# Create a simple URL file
echo "📝 Creating URL file..."
echo "https://quantumnews-ps23.trycloudflare.com" > current_url.txt
echo "https://quantumnews-ps23.trycloudflare.com.3jcllc.com" >> current_url.txt

# Test URLs and find working one
echo "🧪 Testing tunnel URLs..."
WORKING_URL=""

# Test the URLs we know might work
for url in "https://quantumnews-ps23.trycloudflare.com" "https://quantumnews-ps23.trycloudflare.com.3jcllc.com"; do
    echo -n "Testing $url... "
    if curl -s "$url/health" >/dev/null 2>&1; then
        echo "✅ WORKING!"
        WORKING_URL="$url"
        echo "$url" > working_url.txt
        break
    else
        echo "❌"
    fi
done

# If named tunnel doesn't work, try quick tunnel
if [ -z "$WORKING_URL" ]; then
    echo "🔄 Named tunnel not working, trying quick tunnel..."
    pkill -f "cloudflared tunnel"
    sleep 2
    
    cloudflared tunnel --url http://localhost:5004 &
    sleep 10
    
    # Test common quick tunnel URLs
    QUICK_URLS=(
        "https://correspondence-font-about-peninsula.trycloudflare.com"
        "https://morning-way-joins-nov.trycloudflare.com"
        "https://africa-operating-purposes-establishing.trycloudflare.com"
        "https://older-ivory-calculated-massage.trycloudflare.com"
        "https://observations-vacation-biz-received.trycloudflare.com"
        "https://hz-younger-pulled-jewelry.trycloudflare.com"
    )
    
    for url in "${QUICK_URLS[@]}"; do
        echo -n "Testing $url... "
        if curl -s "$url/health" >/dev/null 2>&1; then
            echo "✅ WORKING!"
            WORKING_URL="$url"
            echo "$url" > working_url.txt
            break
        else
            echo "❌"
        fi
    done
fi

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
    echo "🔗 URL saved to: working_url.txt"
    echo "⏹️  To stop: pkill -f 'cloudflared tunnel' && pkill -f 'python.*start_server.py'"
else
    echo ""
    echo "❌ No working URLs found"
    echo "🔧 Try manually: cloudflared tunnel --url http://localhost:5004"
fi















