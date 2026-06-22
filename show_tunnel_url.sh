#!/bin/bash

echo "🌐 Quantum Webscraper - Current Tunnel Status"
echo ""

# Check if tunnel is running
if pgrep -f "cloudflared tunnel" > /dev/null; then
    echo "✅ Tunnel is running"
    echo ""
    echo "🔍 Looking for tunnel URL..."
    echo ""
    
    # Try to get the URL from the tunnel process
    TUNNEL_PID=$(pgrep -f "cloudflared tunnel")
    echo "🆔 Tunnel PID: $TUNNEL_PID"
    echo ""
    
    echo "🌐 Try these URLs:"
    echo "   https://correspondence-font-about-peninsula.trycloudflare.com"
    echo "   https://morning-way-joins-nov.trycloudflare.com"
    echo "   https://quantumnews-ps23.trycloudflare.com"
    echo "   https://quantumnews-ps23.trycloudflare.com.3jcllc.com"
    echo ""
    
    echo "🧪 Testing URLs..."
    for url in "correspondence-font-about-peninsula" "morning-way-joins-nov" "quantumnews-ps23"; do
        full_url="https://$url.trycloudflare.com"
        echo -n "Testing $full_url... "
        if curl -s "$full_url/health" >/dev/null 2>&1; then
            echo "✅ WORKING!"
            echo ""
            echo "🎉 Your webscraper is available at:"
            echo "   $full_url"
            echo ""
            echo "📱 Mobile access: $full_url"
            exit 0
        else
            echo "❌"
        fi
    done
    
    echo ""
    echo "❌ No working URLs found."
    echo "🔧 The tunnel might still be starting up..."
    
else
    echo "❌ No tunnel running"
    echo "🚀 Start the tunnel with:"
    echo "   cloudflared tunnel --url http://localhost:5002"
fi















