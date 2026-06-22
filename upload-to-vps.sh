#!/bin/bash

# Upload Quantum News files to VPS
VPS_IP="155.138.194.149"
VPS_USER="root"
VPS_PATH="/opt/quantum-webscraper"

echo "Uploading files to VPS..."

# Create the directory structure on VPS
ssh $VPS_USER@$VPS_IP "mkdir -p $VPS_PATH"

# Upload key files
scp app.py $VPS_USER@$VPS_IP:$VPS_PATH/
scp requirements.txt $VPS_USER@$VPS_IP:$VPS_PATH/
scp wsgi.py $VPS_USER@$VPS_IP:$VPS_PATH/
scp config.py $VPS_USER@$VPS_IP:$VPS_PATH/

# Upload templates directory
scp -r templates/ $VPS_USER@$VPS_IP:$VPS_PATH/

# Upload static files if they exist
if [ -d "static" ]; then
    scp -r static/ $VPS_USER@$VPS_IP:$VPS_PATH/
fi

# Upload data directory if it exists
if [ -d "data" ]; then
    scp -r data/ $VPS_USER@$VPS_IP:$VPS_PATH/
fi

echo "Files uploaded successfully!"