#!/bin/bash

echo "🌐 Quantum News PS23 - Current Status"
echo ""

if [ -f "working_url.txt" ]; then
    WORKING_URL=$(cat working_url.txt)
    echo "✅ Your webscraper is running!"
    echo ""
    echo "🌐 Current URL:"
    echo "   $WORKING_URL"
    echo ""
    echo "📱 Mobile access: $WORKING_URL"
    echo ""
    echo "🧪 Testing URL..."
    if curl -s "$WORKING_URL/health" >/dev/null 2>&1; then
        echo "✅ URL is working perfectly!"
        echo ""
        echo "🚀 Quick access options:"
        echo "   • Direct: $WORKING_URL"
        echo "   • Branded: Open quantumnews-ps23.html"
        echo ""
        echo "📊 Features available:"
        echo "   • Live market data (S&P 500, NASDAQ, DOW, WTI, Brent, etc.)"
        echo "   • Latest financial news with sentiment analysis"
        echo "   • Portfolio management"
        echo "   • Mobile optimized interface"
    else
        echo "❌ URL not responding"
        echo "🔧 Try restarting the tunnel:"
        echo "   cloudflared tunnel --url http://localhost:8082"
    fi
else
    echo "❌ No working URL found"
    echo "🚀 Start the webscraper:"
    echo "   python start_server.py"
    echo "   cloudflared tunnel --url http://localhost:8082"
fi















