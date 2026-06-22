#!/bin/bash

echo "🌐 Quantum Webscraper - Permanent URL Setup"
echo ""

# Get the tunnel ID
TUNNEL_ID="f78a95c2-e669-4884-a90e-6ea49a609fa9"
HOSTNAME="quantumnews-ps23"

echo "📡 Setting up permanent URL..."
echo "🆔 Tunnel ID: $TUNNEL_ID"
echo "🏷️  Hostname: $HOSTNAME"
echo ""

# Set up the DNS route
echo "🔗 Creating DNS route..."
cloudflared tunnel route dns $TUNNEL_ID $HOSTNAME.trycloudflare.com

echo ""
echo "✅ DNS route created!"
echo "🌐 Your permanent URL is:"
echo "   https://$HOSTNAME.trycloudflare.com.3jcllc.com"
echo ""
echo "🚀 To start the tunnel, run:"
echo "   cloudflared tunnel --config cloudflare-tunnel.yml run quantum-webscraper"
echo ""
echo "📱 Mobile access: https://$HOSTNAME.trycloudflare.com.3jcllc.com"















