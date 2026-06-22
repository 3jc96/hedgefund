#!/bin/bash

echo "🌐 Starting Permanent Cloudflare Tunnel..."
echo "📡 URL: https://quantumnews-ps23.trycloudflare.com"
echo ""

# Stop any existing tunnels
echo "🛑 Stopping existing tunnels..."
pkill -f "cloudflared tunnel" 2>/dev/null
sleep 2

# Start the webscraper if not running
if ! curl -s http://localhost:5002/health >/dev/null 2>&1; then
    echo "🚀 Starting webscraper server..."
    python start_server.py &
    sleep 5
fi

# Start the tunnel with the specific hostname
echo "🚀 Starting permanent tunnel..."
echo "📱 Your webscraper will be available at: https://quantumnews-ps23.trycloudflare.com"
echo "⏹️  Press Ctrl+C to stop"
echo ""

cloudflared tunnel --hostname quantumnews-ps23.trycloudflare.com --url http://localhost:5002















