#!/bin/bash

echo "🌐 Starting Named Cloudflare Tunnel..."
echo "📡 Permanent URL: https://quantumnews-ps23.trycloudflare.com"
echo ""

# Stop any existing tunnels
echo "🛑 Stopping existing tunnels..."
pkill -f "cloudflared tunnel" 2>/dev/null

# Wait a moment
sleep 2

# Start the named tunnel
echo "🚀 Starting named tunnel..."
cloudflared tunnel --config cloudflare-tunnel.yml run quantum-webscraper
