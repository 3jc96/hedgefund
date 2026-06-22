#!/bin/bash
# Cloudflared Installation Script for VPS
# Run this script on your VPS as root or with sudo

set -e

echo "☁️ Installing Cloudflared on VPS..."

# Download and install cloudflared
cd /tmp
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
dpkg -i cloudflared-linux-amd64.deb

# Verify installation
cloudflared version

echo "✅ Cloudflared installed successfully!"
echo ""
echo "Next steps:"
echo "1. Run: cloudflared tunnel login"
echo "2. Run: cloudflared tunnel create quantumnews"
echo "3. Run: cloudflared tunnel route dns quantumnews quantumnews-ps23.3jcllc.com"
echo "4. Copy the tunnel credentials to /etc/cloudflared/"
echo "5. Update the config file with your tunnel ID"











