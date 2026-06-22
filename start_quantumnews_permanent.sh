#!/bin/bash

echo "🌐 Starting Quantum News Webscraper with Permanent URL"
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

# Start tunnel
echo "🌐 Starting Cloudflare tunnel..."
cloudflared tunnel --url http://localhost:8081 &
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
    "https://hz-younger-pulled-jewelry.trycloudflare.com"
    "https://interface-ancient-output-honor.trycloudflare.com"
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
    echo "🔗 URL saved to: working_url.txt"
    echo "$WORKING_URL" > working_url.txt
    
    # Create a simple redirect page for quantumnews-ps23 branding
    echo "📝 Creating quantumnews-ps23 redirect page..."
    cat > quantumnews-ps23.html << EOF
<!DOCTYPE html>
<html>
<head>
    <title>Quantum News PS23 - Redirecting...</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: Arial, sans-serif; text-align: center; padding: 50px; background: #1a1a1a; color: #00d4aa; }
        .container { max-width: 600px; margin: 0 auto; }
        .logo { font-size: 2em; margin-bottom: 20px; }
        .url { background: #333; padding: 15px; border-radius: 5px; margin: 20px 0; word-break: break-all; }
        .button { background: #00d4aa; color: #1a1a1a; padding: 15px 30px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">🌐 Quantum News PS23</div>
        <h2>Your webscraper is ready!</h2>
        <p>Click the button below to access your webscraper:</p>
        <div class="url">$WORKING_URL</div>
        <a href="$WORKING_URL" class="button" target="_blank">🚀 Open Webscraper</a>
        <p><small>This URL will work from anywhere in the world!</small></p>
    </div>
    <script>
        // Auto-redirect after 3 seconds
        setTimeout(function() {
            window.open('$WORKING_URL', '_blank');
        }, 3000);
    </script>
</body>
</html>
EOF
    
    echo "✅ Created quantumnews-ps23.html with your working URL"
    echo ""
    echo "🌐 To access your webscraper:"
    echo "   • Direct URL: $WORKING_URL"
    echo "   • Or open: quantumnews-ps23.html"
    echo ""
    echo "⏹️  To stop: pkill -f 'cloudflared tunnel' && pkill -f 'python.*start_server.py'"
else
    echo ""
    echo "❌ No working URLs found"
    echo "🔧 Try manually: cloudflared tunnel --url http://localhost:8081"
fi















