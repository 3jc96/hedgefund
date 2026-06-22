#!/bin/bash

echo "🔍 Finding current tunnel URL..."
echo ""

# Common tunnel URL patterns
URLS=(
    "https://correspondence-font-about-peninsula.trycloudflare.com"
    "https://morning-way-joins-nov.trycloudflare.com"
    "https://quantumnews-ps23.trycloudflare.com"
    "https://quantumnews-ps23.trycloudflare.com.3jcllc.com"
)

echo "🧪 Testing tunnel URLs..."

for url in "${URLS[@]}"; do
    echo -n "Testing $url... "
    if curl -s "$url/health" >/dev/null 2>&1; then
        echo "✅ WORKING!"
        echo ""
        echo "🌐 Your webscraper is available at:"
        echo "   $url"
        echo ""
        echo "📱 Mobile access: $url"
        exit 0
    else
        echo "❌"
    fi
done

echo ""
echo "❌ No working URLs found."
echo "🔧 Try restarting the tunnel:"
echo "   pkill -f 'cloudflared tunnel'"
echo "   cloudflared tunnel --url http://localhost:5002"

















