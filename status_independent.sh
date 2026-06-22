#!/bin/bash

# Status check script for Quantum News Webscraper

cd /Users/joelchu/quantum-webscraper

echo "📊 Quantum News Webscraper Status"
echo "================================="

# Check Flask app
if [ -f flask.pid ]; then
    FLASK_PID=$(cat flask.pid)
    if ps -p $FLASK_PID > /dev/null 2>&1; then
        echo "✅ Flask app running (PID: $FLASK_PID)"
        
        # Test local connection
        if curl -s http://localhost:8081/qa > /dev/null; then
            echo "   🌐 Local access: http://localhost:8081"
        else
            echo "   ❌ Local access: FAILED"
        fi
    else
        echo "❌ Flask app not running (stale PID file)"
        rm flask.pid
    fi
else
    echo "❌ Flask app not running (no PID file)"
fi

# Check Cloudflare tunnel
if [ -f tunnel.pid ]; then
    TUNNEL_PID=$(cat tunnel.pid)
    if ps -p $TUNNEL_PID > /dev/null 2>&1; then
        echo "✅ Cloudflare tunnel running (PID: $TUNNEL_PID)"
        
        # Test public connection
        if curl -s https://quantumnews-ps23.3jcllc.com/qa > /dev/null; then
            echo "   🌍 Public access: https://quantumnews-ps23.3jcllc.com"
        else
            echo "   ❌ Public access: FAILED"
        fi
    else
        echo "❌ Cloudflare tunnel not running (stale PID file)"
        rm tunnel.pid
    fi
else
    echo "❌ Cloudflare tunnel not running (no PID file)"
fi

echo ""
echo "📝 Recent logs:"
if [ -f flask.log ]; then
    echo "Flask (last 3 lines):"
    tail -3 flask.log | sed 's/^/   /'
fi

if [ -f tunnel.log ]; then
    echo "Tunnel (last 3 lines):"
    tail -3 tunnel.log | sed 's/^/   /'
fi














