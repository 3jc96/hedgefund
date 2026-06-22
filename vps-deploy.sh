#!/bin/bash
# VPS Deployment Script for Quantum News Webscraper
# Run this script on your VPS as root or with sudo

set -e

echo "🚀 Starting VPS deployment for Quantum News Webscraper..."

# Update system
echo "📦 Updating system packages..."
apt update && apt upgrade -y

# Install required packages
echo "🔧 Installing system dependencies..."
apt install -y python3 python3-pip python3-venv nginx git curl wget unzip

# Create application user
echo "👤 Creating application user..."
useradd -m -s /bin/bash quantumnews || echo "User quantumnews already exists"
usermod -aG sudo quantumnews

# Create application directory
echo "📁 Setting up application directory..."
mkdir -p /opt/quantum-webscraper
chown quantumnews:quantumnews /opt/quantum-webscraper

# Switch to application user for next steps
echo "🔄 Switching to application user..."
su - quantumnews << 'EOF'
cd /opt/quantum-webscraper

# Clone or copy application files
echo "📥 Setting up application files..."
# Note: You'll need to upload your files here or clone from git

# Create virtual environment
echo "🐍 Creating Python virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

# Install Python dependencies
echo "📚 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Install Gunicorn
pip install gunicorn

echo "✅ Application setup complete!"
EOF

echo "🎉 VPS deployment script completed!"
echo ""
echo "Next steps:"
echo "1. Upload your application files to /opt/quantum-webscraper"
echo "2. Run the systemd setup script"
echo "3. Configure Cloudflare tunnel"











