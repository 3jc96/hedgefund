#!/bin/bash

echo "🌐 Starting Cloudflare Tunnel with custom hostname..."
echo "📡 URL: https://quantum-news.trycloudflare.com"
echo ""

# Stop any existing tunnels
echo "🛑 Stopping existing tunnels..."
pkill -f "cloudflared tunnel" 2>/dev/null

# Wait a moment
sleep 2

# Start the tunnel with custom hostname
echo "🚀 Starting tunnel with custom hostname..."
cloudflared tunnel --hostname quantum-news.trycloudflare.com --url http://localhost:8081


