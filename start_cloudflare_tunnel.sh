#!/bin/bash

echo "🌐 Starting Cloudflare Tunnel for Quantum Webscraper..."
echo "📡 This will make your webscraper accessible from anywhere!"
echo ""

# Check if tunnel config exists
if [ ! -f "cloudflare-tunnel.yml" ]; then
    echo "❌ Error: cloudflare-tunnel.yml not found"
    exit 1
fi

# Start the tunnel
echo "🚀 Starting tunnel..."
cloudflared tunnel --config cloudflare-tunnel.yml run quantum-webscraper


