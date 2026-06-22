#!/bin/bash

echo "🌐 Quantum News Webscraper - Current URL"
echo ""

if [ -f "working_url.txt" ]; then
    WORKING_URL=$(cat working_url.txt)
    echo "✅ Current working URL:"
    echo "   $WORKING_URL"
    echo ""
    echo "📱 Mobile access: $WORKING_URL"
    echo ""
    echo "🧪 Testing URL..."
    if curl -s "$WORKING_URL/health" >/dev/null 2>&1; then
        echo "✅ URL is working!"
    else
        echo "❌ URL not responding"
        echo "🔧 Try restarting: ./start_quantumnews_tunnel.sh"
    fi
else
    echo "❌ No working URL found"
    echo "🚀 Start the webscraper: ./start_quantumnews_tunnel.sh"
fi















