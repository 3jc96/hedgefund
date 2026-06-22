#!/bin/bash
# Systemd Service Setup Script
# Run this script on your VPS as root or with sudo

set -e

echo "🔧 Setting up systemd services..."

# Create Gunicorn systemd service
cat > /etc/systemd/system/quantumnews.service << 'EOF'
[Unit]
Description=Quantum News Webscraper (Gunicorn)
After=network.target

[Service]
User=quantumnews
Group=quantumnews
WorkingDirectory=/opt/quantum-webscraper
Environment=PORT=8082
ExecStart=/opt/quantum-webscraper/.venv/bin/gunicorn -w 2 -b 127.0.0.1:8082 wsgi:application
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# Create Cloudflared systemd service
cat > /etc/systemd/system/cloudflared.service << 'EOF'
[Unit]
Description=Cloudflare Tunnel
After=network.target

[Service]
Type=simple
User=root
ExecStart=/usr/local/bin/cloudflared tunnel --config /etc/cloudflared/config.yml run quantumnews
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# Create cloudflared config directory
mkdir -p /etc/cloudflared

# Create cloudflared config (you'll need to update the tunnel ID and credentials)
cat > /etc/cloudflared/config.yml << 'EOF'
tunnel: YOUR_TUNNEL_ID_HERE
credentials-file: /etc/cloudflared/YOUR_TUNNEL_ID_HERE.json

ingress:
  - hostname: quantumnews-ps23.3jcllc.com
    service: http://127.0.0.1:8082
  - service: http_status:404
EOF

# Reload systemd and enable services
systemctl daemon-reload
systemctl enable quantumnews
systemctl enable cloudflared

echo "✅ Systemd services configured!"
echo ""
echo "Next steps:"
echo "1. Update /etc/cloudflared/config.yml with your tunnel ID and credentials"
echo "2. Copy your tunnel credentials file to /etc/cloudflared/"
echo "3. Start the services: systemctl start quantumnews cloudflared"











